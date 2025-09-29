from langchain_core.tools import tool
import dask.dataframe as dd
import streamlit as st
import pandas as pd

from app.model.db_cache import DB_CACHE

@tool
async def load_db(
        cache_key: str,

) \
        -> str:
    """
    Always call this tool first
    Use this tool to load database from .csv file
    """
    try:
        uploaded_file = st.session_state["file_input"]

        uploaded_file.seek(0)

        if uploaded_file is not None:
            # pandas ile oku
            df = pd.read_csv(uploaded_file)

            # dask dataframe’e çevir
            ddf = dd.from_pandas(df)

        DB_CACHE[cache_key]["dask_plan"] = ddf

        return f"Database column names: {list(ddf.columns)} , cache_key: {cache_key}"



    except Exception as e:
        return f"call final_answer tool and summarize this error {e} briefly and give instructions about how to solve it "





