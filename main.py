
from fastapi import FastAPI

from chainlit_custom.mount import mount_chainlit_custom

app = FastAPI()


mount_chainlit_custom(app, target="chainlit_apps/app1.py", path="/chainlit")

mount_chainlit_custom(app, target="chainlit_apps/app2.py", path="/chat-copilot")


@app.get("/info")
async def info():
    return {"message": "This is a FastAPI endpoint"}


# Define a simple FastAPI endpoint for testing
@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8088)
