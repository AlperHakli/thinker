import asyncio

import streamlit as st


def initializing_params():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "file_input" not in st.session_state:
        st.session_state["file_input"] = None
    if "badgelabel" not in st.session_state:
        st.session_state["badgelabel"] = "Provide an OpenAI API key"
    if "badgecolor" not in st.session_state:
        st.session_state["badgecolor"] = "yellow"
    if "show_file_input" not in st.session_state:
        st.session_state["show_file_input"] = False
    if "file_uploaded" not in st.session_state:
        st.session_state["file_uploaded"] = False
    if "tool_exec" not in st.session_state:
        st.session_state["tool_exec"] = []
    if "tokens" not in st.session_state:
        st.session_state["tokens"] = []
    if "get_input" not in st.session_state:
        st.session_state["get_input"] = False
    if "is_user_typed" not in st.session_state:
        st.session_state["is_user_typed"] = False
    if "counter" not in st.session_state:
        st.session_state["counter"] = 0
    if "streamer" not in st.session_state:
        st.session_state["streamer"] = "deneme"
    if "expander_content" not in st.session_state:
        st.session_state["expander_content"] = []
    if "agent_name_list" not in st.session_state:
        st.session_state["agent_name_list"] = []
    if "current_agent_name" not in st.session_state:
        st.session_state["current_agent_name"] = "initialized_agent"
    if "visualization_list" not in st.session_state:
        st.session_state["visualization_list"] = []
    if "chat_input_permission" not in st.session_state:
        st.session_state["chat_input_permission"] = False
    if "settings_permission" not in st.session_state:
        st.session_state["settings_permission"] = False
    if "param_width" not in st.session_state:
        st.session_state["param_width"] = 4  # default = 4
    if "param_height" not in st.session_state:
        st.session_state["param_height"] = 3  # default = 3
    if "database" not in st.session_state:
        st.session_state["database"] = ""
    if "last_agent_seen" not in st.session_state:
        st.session_state["last_agent_seen"] = False


