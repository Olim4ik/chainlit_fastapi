# Integrating Chainlit with FastAPI

We have two chainlit endpoints with socket connections:

- /chainlit
- /chat-copilot

We are using this custom middleware to mount the chainlit apps for our AI services in our poject.
We are using socket connections of chainlit as our main socket connections for data exchange between our AI services and the frontend. 
Our Main AI service is chat-copilot, and there are several AI services with automation. 


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




