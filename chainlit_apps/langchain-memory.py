import chainlit as cl
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage
from langchain_core.runnables.config import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

load_dotenv()

# Define the workflow
workflow = StateGraph(state_schema=MessagesState)
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def call_model(state: MessagesState, config: RunnableConfig):
    
    config: RunnableConfig = {
        "configurable": {"thread_id": "1", "user_id": "1"}  # cl.context.session.thread_id
    }
    
    # Print the full current message history for debugging
    print("Full message history:", state["messages"])

    # Limit to the last 10 messages
    recent_messages = state["messages"][-10:]
    print("Recent 10 messages sent to LLM:", recent_messages)

    # Invoke the LLM with only the last 10 messages
    response = model.invoke(recent_messages, config)

    # Return the response to append to the state
    return {"messages": response}


# Add node and edge
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

# Initialize memory and compile the app
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Chat started! How can I assist you?").send()


@cl.on_chat_resume
async def on_chat_resume(thread):
    await cl.Message(content="Resuming chat...").send()


@cl.on_message
async def main(message: cl.Message):
    # Configure the thread ID for the checkpointer
    config: RunnableConfig = {
        "configurable": {"thread_id": "1", "user_id": "1"}  # cl.context.session.thread_id
    }

    # Get the current state (existing message history)
    current_state = await app.aget_state(config)
    current_messages = current_state.values["messages"] if current_state.values else []

    # Append the new message to the existing history
    new_message = HumanMessage(content=message.content)
    updated_messages = current_messages + [new_message]
    
    print("updated_messages", updated_messages)

    # Stream the response with the updated message history
    answer = cl.Message(content="")
    await answer.send()

    for msg, _ in app.stream(
        {"messages": updated_messages},  # Pass the full updated history
        config,
        stream_mode="messages",
    ):
        if isinstance(msg, AIMessageChunk):
            answer.content += msg.content
            await answer.update()

# Run with: chainlit run this_file.py --debug

# @cl.password_auth_callback
# def auth_callback(username: str, password: str):
#     print("Credentials:", username, password)

#     return cl.User(
#         identifier="admin", metadata={"role": "admin", "provider": "credentials"}
#     )
#     # Fetch the user matching username from your database
#     # and compare the hashed password with the value stored in the database
#     if (username, password) == ("admin", "admin"):
#         return cl.User(
#             identifier="admin", metadata={"role": "admin", "provider": "credentials"}
#         )
#     elif (username, password) == ("user", "user"):
#         return cl.User(
#             identifier="user", metadata={"role": "user", "provider": "credentials"}
#         )
#     else:
#         return None
