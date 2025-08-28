from fastapi.responses import StreamingResponse
from config import settings
from app.backend.services.token_generator import token_generator
from app.model.chains.agent_router import agent_router, prompt_embeddings
from app.model.models import embedding_model
from app.model.tools.agents_and_tools import agents_and_tools
from app.model.queue_callback_handler import QueueCallBackHandler
import asyncio
from sqlalchemy.orm import Session
import uuid


config = {"configurable": {
        "k": 2,
        "session_id": uuid.uuid4(),
    }}



async def invoke(userinput : str):
    queue = asyncio.Queue()
    streamer = QueueCallBackHandler(queue=queue)
    embedded_input = embedding_model.embed_query(userinput)
    agent_and_tools = agent_router(
        embedded_input=embedded_input,
        agents_and_tools=agents_and_tools,
        prompt_embeddings=prompt_embeddings,
        agent_names=settings.AGENT_NAMES,
        verbose=True

    )

    return StreamingResponse(
        content=token_generator(
            agent_and_tools=agent_and_tools,
            streamer=streamer,
            input=userinput,
            config= config,
            verbose= True ),
        media_type="text/event-stream"
    )