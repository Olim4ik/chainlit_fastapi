import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    await cl.Message(content=f"Chainlit Socket, message in {__file__}: {message.content}").send()