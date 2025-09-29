# import asyncio
#
#
# from app.model.runner.async_agent_executor import AsyncAgentExecutor
# from app.model.runner.queue_callback_handler import QueueCallBackHandler
# from app.model.tools.agents_and_tools import agents_and_tools_as_list
# from app.model.runner.agent_router import agent_router, embedding_model, prompt_embeddings
# from app.backend.services.token_generator import token_generator
# from app.config import settings
#
# executor = AsyncAgentExecutor(5)
# config = {"configurable": {
#         "k": 2,
#         "session_id": "id12",
#     }}
# TODO this uses old embedding agent router as agent orchestration
#
#
# async def run():
#     queue = asyncio.Queue()
#     streamer = QueueCallBackHandler(queue=queue)
#     while True:
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
#
#         async for token in token_generator(
#             agent_and_tools=agent_and_tool,
#             streamer=streamer,
#             input=userinput,
#             config=config,
#             verbose=False
#         ):
#             print(f"GELEN TOKEN : {token}"  , flush=True , end="")
#
# asyncio.run(run())

