from langchain_core.tools import tool
import dask.dataframe as dd
import pandas as pd
from typing import Union
from pydantic import SkipValidation
from pathlib import Path
from dask.distributed import LocalCluster
from app.model.db_cache import DB_CACHE


@tool
async def final_answer(input: str) -> str:
    """
    Use this tool to respond to the user with his LANGUAGE
    ALWAYS use this tool when you find the final answer and done with your reasoning
    ALWAYS speak same language with user
    """

    return input


@tool
async def load_db(filename: str , db_path: str = None):
    """
    ALWAYS call this tool first
    Use it to get load database from .csv file
    """
    file_key = filename[:-4]
    base_path = Path(db_path) if db_path else Path(__file__).parent.parent.parent.parent / "csv_file_here"
    file_path = base_path / filename
    print(f"FILEPATHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX : {file_path}")

    try:
        df = dd.read_csv(file_path)
        if file_key not in DB_CACHE:
            DB_CACHE[file_key] = df
        return f"file_key : {file_key}, Database loaded : {df}"

    except FileNotFoundError as e:
        return f"call final_answer tool and mention user about filename is incorrect"
    except Exception as e:
        return f"call final_answer tool and summarize this error {e} briefly and give instructions about how to solve it "


