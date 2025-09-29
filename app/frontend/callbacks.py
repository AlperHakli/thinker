import asyncio
import uuid
import openai
import streamlit as st
import os
from app.config import settings
from langchain_openai import ChatOpenAI


config = {"configurable": {
    "k": 2,
    "session_id": uuid.uuid4().hex,
}}


def openai_api_key_callback():
    if st.session_state.openai_apikey_input == "":
        st.session_state["badgelabel"] = "Provide an OpenAI API key"
        st.session_state["badgecolor"] = "yellow"
        st.session_state["file_uploaded"] = False
    else:
        try:
            # to check if openai api key is valid or not
            model = ChatOpenAI(model="gpt-4.1-nano", api_key=st.session_state.openai_apikey_input)
            model.invoke("hi")
        except openai.AuthenticationError:
            st.session_state["badgelabel"] = "Invalid OpenAI API key ❌"
            st.session_state["badgecolor"] = "red"
            st.session_state["chat_input_permission"] = False
            st.session_state["settings_permission"] = False
        except Exception as e:
            st.session_state["badgelabel"] = "Some error occurded check your connection ❌"
            st.session_state["badgecolor"] = "red"
            st.session_state["chat_input_permission"] = False
            st.session_state["settings_permission"] = False
        else:
            st.session_state["badgelabel"] = "OpenAI API key successfully provided ✔️"
            st.session_state["badgecolor"] = "green"
            st.session_state["settings_permission"] = True
            st.session_state["chat_input_permission"] = True
            os.environ["OPENAI_API_KEY"] = st.session_state.openai_apikey_input



    st.session_state["show_file_input"] = True


def file_upload_callback():
    st.session_state["file_uploaded"] = True
    if st.session_state["file_input"] is None:
        st.session_state["file_input"] = st.session_state["file_uploader"]








async def arun():
    from app.model.runner.agent_router_new import graph_app
    await graph_app.ainvoke({"user_prompt": st.session_state.user_query})

def chat_input_callback():
    asyncio.run(arun())

    st.session_state.is_user_typed = True

def selected_model_name_callback():
    os.environ["OPENAI_MODEL_NAME"] = st.session_state.model_selector

def size_change_callback():
    try:
        width = float(st.session_state.param_width)
    except ValueError:
        width = 4.0

    try:
        height = float(st.session_state.param_height)
    except ValueError:
        height = 3.0

    settings.VISUALIZATION_SIZE = (width, height)


