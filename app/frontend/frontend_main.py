import ast
import asyncio
import os
import sys



PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from app.frontend.callbacks import chat_input_callback
import pandas as pd
import streamlit as st
from PIL import Image

from app.frontend import callbacks , constants , initializing_params


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# page configuration
st.set_page_config(
    page_title="Thinker",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon=Image.open("app/frontend/icon.png"),

)

# parameter initialization
initializing_params.initializing_params()

st.markdown(
    f'''
    <div style="display: flex; justify-content: flex-start; align-items: flex-start; margin: -50px 10px 0 10px;">
        <h1 style="margin:0;">🤖 {constants.colored_title}</h1>
    </div>
    ''',
    unsafe_allow_html=True
)

st.markdown(
    f'''
    <div style="display: flex; justify-content: flex-start; align-items: flex-start; margin: -10px 10px 0 10px;">
        <p style="margin:0;">Upload your csv database to visualization or analyze based on prompt</p>
    </div>
    ''',
    unsafe_allow_html=True
)

st.divider()

if st.session_state["settings_permission"] == False:
    st.badge(label=st.session_state.badgelabel, width="stretch", color=st.session_state.badgecolor)
else:
    col1 , col2 = st.columns(2)
    with col1:
        st.badge(label=st.session_state.badgelabel, width="stretch", color=st.session_state.badgecolor)
    with col2:
        with st.expander("Settings" , width=300):
            with st.expander("Model Name"):
                selected_model = st.selectbox(
                    "Choose a model",
                    ["gpt-4.1-nano", "gpt-4.1-mini", "gpt-4.1", "gpt-4o"],
                    key="model_selector",
                    on_change= callbacks.selected_model_name_callback,
                )

            with st.expander("Adjust the size of Images"):
                st.text_input(label=" ",label_visibility="hidden",placeholder="Width (Default 4)" , key="param_width" , on_change=callbacks.size_change_callback)
                st.text_input(label=" ",label_visibility="hidden",placeholder="Height (Default 3)" , key="param_height" , on_change=callbacks.size_change_callback)






openai_api_key = st.text_input(label=" ", placeholder="OpenAI API key", key="openai_apikey_input",
                               on_change=callbacks.openai_api_key_callback, type="password")

if st.session_state["show_file_input"]:
    file = st.file_uploader(label="Upload your .csv database or drag it", on_change=callbacks.file_upload_callback,
                            type="csv" , accept_multiple_files= False , key="file_uploader")

    if st.session_state["file_uploaded"]:
        st.badge(label="File successfully uploaded ✔️", color="green")
        st.divider()
        db = pd.read_csv(file)
        st.write(db)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Rows")
            rownum = db.shape[0]
            st.write(f"{rownum}")
        with col2:
            st.write("Columns")
            colnum = db.shape[1]
            st.write(f"{colnum}")
        with col3:
            st.write("Different Dtypes")
            st.write(f"{db.dtypes.nunique()}")
        st.divider()

        if st.session_state["chat_input_permission"]:
            st.title("Data Insights 📊📈")
            chat_input = st.text_input("Your query", key="user_query", on_change=chat_input_callback)



    if "token_queue" not in st.session_state:
        st.session_state["token_queue"] = asyncio.Queue()

    if st.session_state.is_user_typed:
        st.write_stream(st.session_state.streamer)
    st.session_state.counter += 1
    counter = 0
    if not st.session_state["current_agent_name"] == "initialized_agent":
        st.balloons()
        for contents in st.session_state["expander_content"]:
            counter += 1
            # current agent name that writes into header of expander
            agent_name = contents.get("current_agent_name")
            # AIMessageChunk that belongs to current agent
            contentlist = contents.get("contentlist")
            print(type(agent_name))
            print(type(contentlist))
            print(contentlist)
            with st.expander(agent_name):
                for content in contentlist:
                    tool_call = content.additional_kwargs.get("tool_calls")[0].get("function")
                    argdict = ast.literal_eval(tool_call.get("arguments"))
                    with st.expander(tool_call.get("name")):
                        for key, value in argdict.items():
                            st.write("{" + f"'{key}':'{value}'" + "}")
        st.session_state["expander_content"] = []
    if not st.session_state["visualization_list"] == []:
        for fig in st.session_state["visualization_list"]:
            st.pyplot(fig=fig, width="content")
        st.session_state["visualization_list"] = []





