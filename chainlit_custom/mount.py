
import os

from chainlit.config import config, load_module
from chainlit.server import app as chainlit_app
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


# Define a custom middleware for each Chainlit app
class ChainlitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, path, target):
        super().__init__(app)
        self.path = path.rstrip('/')
        self.target = target

    async def dispatch(self, request: Request, call_next):
        # Ensure the request path matches the intended subpath
        if not request.url.path.startswith(self.path):
            return JSONResponse(status_code=404, content={"detail": "Not found"})

        # Load the correct module for this request
        # We reset module_name per request to avoid conflicts
        config.run.module_name = self.target
        try:
            load_module(self.target)
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

        return await call_next(request)


def mount_chainlit_custom(fastapi_app: FastAPI, target: str, path: str):
    # Configure Chainlit for this specific instance
    config.run.debug = os.environ.get("CHAINLIT_DEBUG", False)

    # Create a new FastAPI sub-app to isolate middleware
    sub_app = FastAPI()
    sub_app.mount("/", chainlit_app)

    # Add middleware specific to this path
    sub_app.add_middleware(ChainlitMiddleware, path=path, target=target)

    # Mount the sub-app
    fastapi_app.mount(path, sub_app)
