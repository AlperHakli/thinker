import uuid
from app.model.db_cache import DB_CACHE
from app.model.runner.async_agent_executor import AsyncAgentExecutor
from app.model.tools.agents_and_tools import agents_and_tools
from app.model.utils.typed_dictionaries import GeneralState, SingleState
import asyncio
from app.model.runner.queue_callback_handler import QueueCallBackHandler
import streamlit as st
from app.model.tools.tool_list import database_analysis_agent_toollist, database_visualization_agent_toollist

executor = AsyncAgentExecutor(10)

config = {"configurable": {
    "k": 2,
    "session_id": uuid.uuid4().hex,
}}

"""this file contains all agents as langgraph nodes
I couldn't find a way to write simpler than this
With this code token_generator.py is unnecessary I will delete it next update"""


#single mydict that contains agent name and its duckduck


# Chat agent node

async def chat_agent_node(general_state: GeneralState):
    # print(f"GENERAL STATE IN CHAT NODE: {general_state}")
    queue = asyncio.Queue()
    streamer = QueueCallBackHandler(queue=queue)
    task = asyncio.create_task(
        executor.ainvoke(
            agent_and_tools=agents_and_tools["chat_agent"],
            streamer=streamer,
            input=general_state["user_prompt"],
            cache_key=general_state["cache_key"],
            config=config,
            verbose=False))
    st.session_state["current_agent_name"] = "Chat Agent"
    tool_exec = await task
    st.session_state["tool_exec"] = tool_exec

    async_gen = streamer.__aiter__()

    st.session_state["streamer"] = async_gen

    single_state = SingleState(agent_name="chat_agent", agent_result=tool_exec)
    # print(f"OBSERVATİONS: {general_state["observations"]}")
    general_state["observations"].append(single_state)

# Math agent node
async def math_agent_node(general_state: GeneralState):
    queue = asyncio.Queue()
    streamer = QueueCallBackHandler(queue=queue)
    task = asyncio.create_task(
        executor.ainvoke(
            agent_and_tools=agents_and_tools["math_agent"],
            streamer=streamer,
            input=general_state["user_prompt"],
            cache_key=general_state["cache_key"],
            config=config,
            verbose=False))
    st.session_state["current_agent_name"] = "Math Agent"
    tool_exec = await task
    async_gen = streamer.__aiter__()

    st.session_state["streamer"] = async_gen
    single_state = SingleState(agent_name="math_agent", agent_result=tool_exec)
    general_state["observations"].append(single_state)


# Data visualization agent node
async def data_visualization_node(general_state: GeneralState):
    queue = asyncio.Queue()
    streamer = QueueCallBackHandler(queue=queue)
    task = asyncio.create_task(
        executor.ainvoke(
            # TODO solve this logical error
            agent_and_tools=agents_and_tools["data_visualization_agent"]
            if DB_CACHE[general_state["cache_key"]]["agent_counter"] ==1
            # that means this visualization agent will use previous agent's result
            else agents_and_tools["data_visualization_agent_dependent"],
            streamer=streamer,
            input=general_state["user_prompt"],
            cache_key=general_state["cache_key"],
            config=config,
            verbose=False))

    st.session_state["current_agent_name"] = "Database Visualization Agent"
    tool_exec = await task

    async_gen = streamer.__aiter__()

    st.session_state["streamer"] = async_gen
    single_state = SingleState(agent_name="data_visualization_agent", agent_result=tool_exec)
    general_state["observations"].append(single_state)



# Data analysis agent node
async def data_analysis_node(general_state: GeneralState):
    queue = asyncio.Queue()
    streamer = QueueCallBackHandler(queue=queue)
    task = asyncio.create_task(
        executor.ainvoke(
            agent_and_tools=agents_and_tools["data_analysis_agent"],
            streamer=streamer,
            input=general_state["user_prompt"],
            cache_key=general_state["cache_key"],
            config=config,
            verbose=False))

    st.session_state["current_agent_name"] = "Database Analysis Agent"
    tool_exec = await task

    async_gen = streamer.__aiter__()

    st.session_state["streamer"] = async_gen
    print(f"DATA ANALYSİS NODE TASK RESULT: {task.result()}")
    single_state = SingleState(agent_name="data_analysis_agent", agent_result=tool_exec)
    general_state["observations"].append(single_state)


# Utility agent node
async def utility_agent_node(general_state: GeneralState):
    queue = asyncio.Queue()
    streamer = QueueCallBackHandler(queue=queue)
    task = asyncio.create_task(
        executor.ainvoke(
            agent_and_tools=agents_and_tools["utility_agent"],
            streamer=streamer,
            input=general_state["user_prompt"],
            cache_key=general_state["cache_key"],
            config=config,
            verbose=False))

    st.session_state["current_agent_name"] = "Utility Agent"
    tool_exec = await task

    async_gen = streamer.__aiter__()

    st.session_state["streamer"] = async_gen
    single_state = SingleState(agent_name="utility_agent", agent_result=tool_exec)
    general_state["observations"].append(single_state)

async def agent_streamer(general_state: GeneralState , agent_name: str):
    """
    General agent executor for langgraph nodes\n
    :param general_state:State dictionary which stores important variables all across in compiled graph\n
    :param agent_name: name of the agent that will execute\n
    :yield: llm response tokens
    """

    if agent_name == "data_visualization_agent":
        if not DB_CACHE[general_state["cache_key"]]["agent_counter"] ==1:
            agent_name = "data_visualization_agent_dependent"

    queue = asyncio.Queue()
    streamer = QueueCallBackHandler(queue=queue)
    task = asyncio.create_task(
        executor.ainvoke(
            agent_and_tools=agents_and_tools[agent_name],
            streamer=streamer,
            input=general_state["user_prompt"],
            cache_key=general_state["cache_key"],
            config=config,
            verbose=False))

    tool_exec = await task
    st.session_state["streamer"] = streamer
    single_state = SingleState(agent_name=agent_name, agent_result=tool_exec)
    general_state["observations"].append(single_state)
