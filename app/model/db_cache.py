from app.model.utils.typed_dictionaries import DbCacheDict
from typing import Dict
import uuid

# it will store cache_key globally in agent_router_new.py setup node will pass an unique id in here


# main cache file that stores variables and user_prompt
DB_CACHE: Dict[str, DbCacheDict] = {}
