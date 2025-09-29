from typing import Union
from app.model.db_cache import DB_CACHE
import pandas as pd
from langchain_core.tools import tool
import streamlit as st
import dask.dataframe as dd


@tool
async def get_correlation(
        cache_key: str,
        column_names: list[str] = None,

) \
        -> Union[dict, str]:
    """
    Use This tool ONLY If you see 'correlation' key in the prompt


    <database> database to use
    <column_names> : name of the columns that user provided for calculating correlation
    """
    try:
        if not "dask_plan" in DB_CACHE[cache_key]:
            uploaded_file = st.session_state["file_input"]

            uploaded_file.seek(0)

            if uploaded_file is not None:
                # pandas ile oku
                df = pd.read_csv(uploaded_file)

                # dask dataframe’e çevir
                ddf = dd.from_pandas(df)

            DB_CACHE[cache_key]["dask_plan"] = ddf
        database = DB_CACHE[cache_key]["dask_plan"]
        database = database.select_dtypes(include="number")
        # ekstra_string = ""
        # if not pd.api.types.is_numeric_dtype(database):
        # database = database.select_dtypes(include="number")
        # ekstra_string = "mention about that you have successfully deleted non-numeric columns with user's language"

        if column_names is None:
            temp = {"correlation": database.corr().compute()}
        else:
            temp = {"correlation": database[column_names].corr().compute()}
        print(f"CACHE KEY VARİABLE AT GET_CORRELATİON: {cache_key}")
        DB_CACHE[cache_key]["analysis_result"].update(temp)
        DB_CACHE[cache_key]["variable_names"].append("correlation")
        if DB_CACHE[cache_key]["agent_counter"] == DB_CACHE[cache_key]["max_agent_count"]:
            return temp
        else:
            return ""


    except Exception as e:
        return f"call the final_answer tool and mention about this error {e} to user"
