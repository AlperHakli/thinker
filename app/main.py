import asyncio


from app.model.async_agent_executor import AsyncAgentExecutor
from app.model.queue_callback_handler import QueueCallBackHandler
from app.model.tools.agents_and_tools import agents_and_tools
from app.model.chains.agent_router import agent_router, embedding_model, prompt_embeddings
from app.backend.services.token_generator import token_generator
from config import settings
from dask.distributed import LocalCluster



executor = AsyncAgentExecutor(5)
config = {"configurable": {
        "k": 2,
        "session_id": "id12",
    }}


async def run():
    while True:
        queue = asyncio.Queue()
        streamer = QueueCallBackHandler(queue=queue)
        userinput = input("Type: ")
        embedded_input = embedding_model.embed_query(userinput)
        agent_and_tool = agent_router(
            embedded_input=embedded_input,
            agents_and_tools=agents_and_tools,
            prompt_embeddings=prompt_embeddings,
            agent_names=settings.AGENT_NAMES,
            verbose=True

        )
        result = await executor.ainvoke(
            agent_and_tools=agent_and_tool,
            streamer=streamer,
            input = userinput,
            config=config,
            verbose=False
        )
        print(f"RESULT İS : {result}")

async def run2():
    queue = asyncio.Queue()
    streamer = QueueCallBackHandler(queue=queue)
    while True:
        userinput = input("Type: ")
        embedded_input = embedding_model.embed_query(userinput)
        agent_and_tool = agent_router(
            embedded_input=embedded_input,
            agents_and_tools=agents_and_tools,
            prompt_embeddings=prompt_embeddings,
            agent_names=settings.AGENT_NAMES,
            verbose=True

        )

        async for token in token_generator(
            agent_and_tools=agent_and_tool,
            streamer=streamer,
            input=userinput,
            config=config,
            verbose=False
        ):
            print(f"GELEN TOKEN : {token}"  , flush=True , end="")

asyncio.run(run2())

# from fastapi import FastAPI
# from app.backend.routers import model_router
# from app.backend.database import Base, engine
#
# Base.metadata.create_all(bind=engine)
#
# app = FastAPI()
#
# app.include_router(model_router.router)
