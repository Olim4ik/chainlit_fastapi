import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    await cl.Message(content=f"Received in App2: {message.content}").send()