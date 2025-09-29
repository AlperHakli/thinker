import asyncio


from app.model.runner.async_agent_executor import AsyncAgentExecutor
from app.model.runner.queue_callback_handler import QueueCallBackHandler
from app.model.tools.agents_and_tools import agents_and_tools_as_list
from app.model.runner.agent_router import agent_router, embedding_model, prompt_embeddings
from app.backend.services.token_generator import token_generator
from app.config import settings

executor = AsyncAgentExecutor(5)
config = {"configurable": {
        "k": 2,
        "session_id": "id12",
    }}


# async def run():
#     while True:
#         queue = asyncio.Queue()
#         streamer = QueueCallBackHandler(queue=queue)
#         userinput = input("Type: ")
#         embedded_input = embedding_model.embed_query(userinput)
#         agent_and_tool = agent_router(
#             embedded_input=embedded_input,
#             agents_and_tools_list=agents_and_tools_as_list,
#             prompt_embeddings=prompt_embeddings,
#             agent_names=settings.AGENT_NAMES,
#             verbose=True
#
#         )
#         duckduck = await executor.ainvoke(
#             agent_and_tools=agent_and_tool,
#             streamer=streamer,
#             input = userinput,
#             config=config,
#             verbose=False
#         )
#         print(f"RESULT İS : {duckduck}")

async def run2():
    queue = asyncio.Queue()
    streamer = QueueCallBackHandler(queue=queue)
    while True:
        userinput = input("Type: ")
        embedded_input = embedding_model.embed_query(userinput)
        agent_and_tool = agent_router(
            embedded_input=embedded_input,
            agents_and_tools_list=agents_and_tools_as_list,
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
# from graph_app.backend.routers import model_router
# from graph_app.backend.database import Base, engine
#
# Base.metadata.create_all(bind=engine)
#
# graph_app = FastAPI()
#
# graph_app.include_router(model_router.router)
