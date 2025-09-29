import asyncio
import json
from langgraph.graph import StateGraph, START, END
from app.model.db_cache import DB_CACHE
from app.model.utils.typed_dictionaries import GeneralState, DbCacheDict
from app.model.chains.raw_chains import supervisor_agent
from app.model.runner import all_agent_nodes
import streamlit as st
import ast
import uuid


def setup_node(general_state: GeneralState) \
        -> GeneralState:
    cache_key = uuid.uuid4().hex
    general_state["observations"] = []
    general_state["cache_key"] = cache_key
    DB_CACHE[cache_key] = {}
    DB_CACHE[cache_key]["agent_counter"] = 0
    DB_CACHE[cache_key]["analysis_result"] = {}
    DB_CACHE[cache_key]["variable_names"] = []
    return general_state


def supervisor_node(general_state: GeneralState) \
        -> GeneralState:
    try:
        cache_key = general_state[("cache_key")]
        # supervisor -> analysis -> supervisor (obs gathered from analysis) -> visualization -> error

        agent_response = supervisor_agent.invoke(
            {
                "agent_history": general_state["observations"],
                "query": general_state["user_prompt"]
            }
        )
        dict_format = agent_response.content.replace("false", "False").replace("true", "True").strip()
        mylist = dict_format.replace("\n", "").split("{")
        mystr = f"{{{mylist[-1]}"
        result = ast.literal_eval(mystr)
        agent_sequence = result["agent_sequence"]
        general_state["current_agent_name"] = agent_sequence[0]
        if len(agent_sequence) == 1:
            st.session_state["last_agent_seen"] = True
        DB_CACHE[cache_key]["agent_counter"] += 1
        if not DB_CACHE[cache_key].get("max_agent_count"):
            DB_CACHE[cache_key]["max_agent_count"] = len(agent_sequence)
        print(
            f" AGENT COUNTER: {DB_CACHE[cache_key]["agent_counter"]} , MAX AGENT COUNT: {DB_CACHE[cache_key]["max_agent_count"]}")
        if DB_CACHE[cache_key]["agent_counter"] == DB_CACHE[cache_key]["max_agent_count"] + 1:
            general_state["current_agent_name"] = "exit"
            return general_state

        print(f"AGENT RESPONSE: {agent_response.content}")

        return general_state
    except Exception as e:
        print(e)
        general_state["current_agent_name"] = "exit"
        return general_state


def node_router(general_state: GeneralState)\
        -> str:
    if general_state["current_agent_name"] == "exit":
        return "exit"
    elif general_state["current_agent_name"] == "chat_agent":
        return "chat_agent"
    # for now, I don't use utility_agent and math_agent because model confuses them with database agents
    # elif general_state["current_agent_name"] == "math_agent":
    #     return "math_agent"

    # elif general_state["current_agent_name"] == "utility_agent":
    #     return "utility_agent"
    elif general_state["current_agent_name"] == "db_analysis_agent":
        return "data_analysis_agent"
    elif general_state["current_agent_name"] == "db_viz_agent":
        return "data_visuzalization_agent"
    else:
        print("Something happened that the dev couldn't think of")
        return "exit"


graph = StateGraph(state_schema=GeneralState)

#NODES:
graph.add_node(node="setup_node", action=setup_node)
graph.add_node(node="supervisor_agent", action=supervisor_node)
graph.add_node(node="chat_agent", action=all_agent_nodes.chat_agent_node)
# graph.add_node(node="math_agent", action=all_agent_nodes.math_agent_node)
# graph.add_node(node="utility_agent", action=all_agent_nodes.utility_agent_node)
graph.add_node(node="data_analysis_agent", action=all_agent_nodes.data_analysis_node)
graph.add_node(node="data_visuzalization_agent", action=all_agent_nodes.data_visualization_node)

#EDGES
graph.add_edge(start_key=START, end_key="setup_node")
graph.add_edge(start_key="setup_node", end_key="supervisor_agent")

graph.add_conditional_edges(
    source="supervisor_agent",
    path=node_router,
    path_map={
        "chat_agent": "chat_agent",
        # "utility_agent": "utility_agent",
        # "math_agent": "math_agent",
        "data_analysis_agent": "data_analysis_agent",
        "data_visuzalization_agent": "data_visuzalization_agent",
        "exit": END
    }
)

graph.add_edge(start_key="chat_agent", end_key="supervisor_agent")
# graph.add_edge(start_key="math_agent", end_key="supervisor_agent")
# graph.add_edge(start_key="utility_agent", end_key="supervisor_agent")
graph.add_edge(start_key="data_analysis_agent", end_key="supervisor_agent")
graph.add_edge(start_key="data_visuzalization_agent", end_key="supervisor_agent")

graph_app = graph.compile()


