# Integrating Chainlit with FastAPI

We have two chainlit endpoints with socket connections:

- /chainlit
- /chat-copilot

We are using this custom middleware to mount the chainlit apps for our AI services in our poject.
We are using socket connections of chainlit as our main socket connections for data exchange between our AI services and the frontend. 
Our Main AI service is chat-copilot, and there are several AI services with automation. 


### About chainlit as a tool

Chainlit is a good library for building chatbots.
It have nice built-in tools for building chatbased applications (Streaming, Action buttons, Elements, etc.).
You can use chainlit fully with python for chat apps, 
or you can use python chainlit service as a BFF (Backend for Frontend) for your React app in the frontend.

Chainlit have well organized socket for sharing data between the frontend and the backend.
You can make some customizations based on your needs.

You can build anything from simple RAG Q&A to complex multi-agent applications.


## How to run

```bash
pip install -r requirements.txt
```

```bash
python main.py
```

## How to run with uvicorn

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8088
```

## How to run chainlit apps separately

```bash
chainlit run chainlit_apps/app1.py
```

```bash
chainlit run chainlit_apps/app2.py
```




