from langchain_core.tools import tool
from typing import Union
import pandas as pd
from app.model.db_cache import DB_CACHE
import streamlit as st
import dask.dataframe as dd


def pandas_series_to_dict(series: pd.Series , variable: str) \
        -> dict:
    tempdict = {}
    for key, value in series.items():
        tempdict[key] = round(value , 3)

    return tempdict


@tool
async def get_median_mean_std_var_min_max_mode(
        cache_key: str,
        stats: list[str],
        column_names: list[str] = True,

) \
        -> Union[dict, str]:
    """
    Use it to calculate mean , median variance minimum maximum mode unique_counts and standard deviation
    stats: mean , median , standard_deviation , variance , minimum , maximum , mode , unique_counts
    :param column_names : name of the columns that user provided for calculating
    :param stats : booleans to select which stats to compute depends on user's purpose
    your stats: [mean, median, standard_deviation ,variance , minimum , maximum , mode , unique_counts]
    mode means the most repeated value in a dataset
    unique_count means count of the unique values in the dataset
    """
    try:

        temp = {}
        # sometimes llm forget to call load_db, but we already have a file input at frontend, so we can use it
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
        # ekstra_string = ""
        # if not pd.api.types.is_numeric_dtype(database):
        #     database = database.select_dtypes(include="number")
        #     ekstra_string = "mention about that you have succesfully deleted non numeric columns with user's language"

        database = database.select_dtypes(include="number")

        if column_names is None:
            for stat in stats:
                if stat == "mean":
                    temp["mean"] = pandas_series_to_dict(database.mean().compute(), variable="mean")
                if stat == "standard_deviation":
                    temp["standard_deviation"] = pandas_series_to_dict(database.std().compute(),
                                                                       variable="standard_deviation")
                if stat == "median":
                    temp["median"] = pandas_series_to_dict(database.median().compute(), variable="median")
                if stat == "variance":
                    temp["variance"] = pandas_series_to_dict(database.var().compute(), variable="varience")
                if stat == "minimum":
                    temp["minimum"] = pandas_series_to_dict(database.min().compute(), variable="minimum")
                if stat == "maximum":
                    temp["maximum"] = pandas_series_to_dict(database.max().compute(), variable="maximum")
                if stat == "mode":
                    temp["mode"] = pandas_series_to_dict(database.mode().compute().loc[0, :], variable="mode")
                if stat == "unique_counts":
                    temp["unique_counts"] = pandas_series_to_dict(database.nunique().compute(),
                                                                  variable="unique_counts")
        else:
            for stat in stats:
                if stat == "mean":
                    temp["mean"] = pandas_series_to_dict(database[column_names].mean().compute(), variable="mean")
                if stat == "standard_deviation":
                    temp["standard_deviation"] = pandas_series_to_dict(database[column_names].std().compute(),
                                                                       variable="standard_deviation")
                if stat == "median":
                    temp["median"] = pandas_series_to_dict(database[column_names].median().compute(), variable="median")
                if stat == "variance":
                    temp["variance"] = pandas_series_to_dict(database[column_names].var().compute(),
                                                             variable="varience")
                if stat == "minimum":
                    temp["minimum"] = pandas_series_to_dict(database[column_names].min().compute(), variable="minimum")
                if stat == "maximum":
                    temp["maximum"] = pandas_series_to_dict(database[column_names].max().compute(), variable="maximum")
                if stat == "mode":
                    temp["mode"] = pandas_series_to_dict(database[column_names].mode().compute().loc[0, :],
                                                         variable="mode")
                if stat == "unique_counts":
                    temp["unique_counts"] = pandas_series_to_dict(database[column_names].nunique().compute(),
                                                                  variable="unique_counts")
        DB_CACHE[cache_key]["analysis_result"].update(temp)
        DB_CACHE[cache_key]["variable_names"].extend(temp.keys())
        if DB_CACHE[cache_key]["agent_counter"] == DB_CACHE[cache_key]["max_agent_count"]:
            return temp
        else:
            return ""




    except Exception as e:
        if not len(temp) == 0:
            return f"Call ONLY the `final_answer` tool. In the response, explain the error: {e}, and provide steps for the user to solve it. also return {temp}"
        return f"Call ONLY the `final_answer` tool. In the response, explain the error: {e}, and provide steps for the user to solve it."



