from langchain_core.tools import tool
import pandas as pd
from typing import Union
from pyarrow.lib import ArrowNotImplementedError
from pydantic import SkipValidation
import dask.dataframe as dd
from app.model.db_cache import DB_CACHE


@tool
async def get_median_mean_std_var_min_max_mode(
        file_key: str,
        column_names: list[str] = True,
        mean: bool = False,
        median: bool = False,
        standard_deviation: bool = False,
        varience: bool = False,
        minimum: bool = False,
        maximum: bool = False,
        mode: bool = False,
        unique_counts: bool = False,
        quantile_value: float = None,

) \
        -> Union[dict, str]:
    """
    Use it to calculate Mean , Median and Standart Deviation

    :param file_key : key value of the database
    :param column_names : name of the columns
    :param mean, median, standard_deviation ,varience , minimum , maximum , mode , unique_counts : booleans to select which stats to compute depends on user's purpose
    quantile_value the quantile value of a numeric column in a dataset.
    mode means the most repeated value in a dataset
    unique_count means count of the unique values in the dataset
    """
    database = DB_CACHE[file_key]
    database = database.select_dtypes(include="number")

    temp = {}
    try:
        if column_names is None:
            if mean:
                temp["mean"] = database.mean().compute()
            if standard_deviation:
                temp["standart_deviation"] = database.std().compute()
            if median:
                temp["median"] = database.median().compute()
            if varience:
                temp["varience"] = database.var().compute()
            if minimum:
                temp["minimum"] = database.min().compute()
            if maximum:
                temp["maximum"] = database.max().compute()
            if mode:
                temp["mode"] = database.mode().loc[0].compute()
            if unique_counts:
                temp["unique_counts"] = database.nunique().compute()
            if quantile_value:
                if quantile_value>1:
                    quantile_value = quantile_value/10
                if quantile_value<0:
                    return "call the final answer and mention about that quantile value cannot smaller than zero"
                temp["quantile_answer"] = database.quantile(quantile_value).compute()


        else:
            if mean:
                temp["mean"] = database[column_names].mean().compute()
            if standard_deviation:
                temp["standart_deviation"] = database[column_names].std().compute()
            if median:
                temp["median"] = database[column_names].median().compute()
            if varience:
                temp["varience"] = database[column_names].var().compute()
            if minimum:
                temp["minimum"] = database[column_names].min().compute()
            if maximum:
                temp["maximum"] = database[column_names].max().compute()
            if mode:
                temp["mode"] = database[column_names].mode().loc[0].compute()
            if unique_counts:
                temp["unique_counts"] = database[column_names].nunique().compute()
            if quantile_value:
                if quantile_value>1:
                    quantile_value = quantile_value/10
                if quantile_value<0:
                    return "call the final answer and mention about that quantile value cannot smaller than zero"
                temp["quantile_answer"] = database[column_names].quantile(quantile_value).compute()

        return temp

    except Exception as e:
        if temp:
            return f"call the final_answer tool and mention about this error {e} to user also return {temp}"
        return f"call the final_answer tool and mention about this error {e} to user"


@tool
async def get_correlation(
        file_key: str,
        column_names: list[str] = None,
        for_visualization: bool = False

) \
        -> Union[pd.DataFrame, str]:
    """
    Use it to return correlation matrix of provided database
    <database> database to use
    <column_names> name of columns that user provided
    <for_visualization> if user want to visualize this correlation's result then set it True
    """
    try:
        database = DB_CACHE[file_key]
        database = database.select_dtypes(include=["number"])
        if column_names is None:
            if for_visualization:
                return database.corr()
            return database.corr().compute()
        if for_visualization:
            return database[column_names].corr()
        return database[column_names].corr().compute()
    except Exception as e:
        return f"call the final_answer tool and mention about this error {e} to user"
