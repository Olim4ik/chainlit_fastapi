import chainlit as cl
from chainlit.sync import run_sync
from langchain.agents import AgentExecutor, AgentType, Tool, initialize_agent
from langchain.chains.llm_math.base import LLMMathChain
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI


class HumanInputChainlit(BaseTool):
    """Tool that adds the capability to ask user for input."""

    name: str = "human"
    description: str = (
        "You can ask a human for guidance when you think you "
        "got stuck or you are not sure what to do next. "
        "The input should be a question for the human."
    )

    def _run(
        self,
        query: str,
        run_manager=None,
    ) -> str:
        """Use the Human input tool."""
        res = run_sync(cl.AskUserMessage(content=query).send())
        return res["content"]

    async def _arun(
        self,
        query: str,
        run_manager=None,
    ) -> str:
        """Use the Human input tool."""
        res = await cl.AskUserMessage(content=query).send()
        return res["output"]


@cl.on_chat_start
def start():
    llm = ChatOpenAI(temperature=0, streaming=True, model_name="gpt-4-turbo-preview")
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

    tools = [
        HumanInputChainlit(),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math",
            coroutine=llm_math_chain.arun,
        ),
    ]
    # Initialize the agent with AgentExecutor explicitly and handle parsing errors
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,  # Add this to handle parsing errors
    )

    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")
    res = await agent.arun(
        message.content, callbacks=[cl.AsyncLangchainCallbackHandler()]
    )
    print(res)
    await cl.Message(content=res).send()
