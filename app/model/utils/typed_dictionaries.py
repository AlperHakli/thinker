from typing import TypedDict, List, Dict
import dask.dataframe as dd

import pandas as pd

from app.model.runner.queue_callback_handler import QueueCallBackHandler


class SingleState(TypedDict):
    agent_name: str
    agent_result: str


#general general_state that contains  agent results , current agent name and cache_key which indicates the agent is last agent in reasoning chain
class GeneralState(TypedDict):
    observations: List[SingleState]
    user_prompt: str
    current_agent_name: str
    cache_key: str


class DbCacheDict(TypedDict, total=False):
    agent_counter: int
    max_agent_count: int
    dask_plan: dd.DataFrame
    analysis_result: Dict
    variable_names: List[str]
