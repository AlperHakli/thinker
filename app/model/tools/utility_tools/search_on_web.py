from langchain_community.utilities import SerpAPIWrapper
from typing import Union
import aiohttp
from langchain_core.tools import tool
from app.config import settings
@tool
async def search_on_web(input: str) \
        -> Union[str, ValueError]:
    """
    Use this tool when user wants to search something on web
    If you find an error then return like you are sorry you can't connect the internet now
    """

    try:
        search = SerpAPIWrapper(serpapi_api_key=settings.SERPAPI_API_KEY)
        result = await search.arun(query=input)
        return result
    except ValueError as e:
        if "Invalid API key" in str(e):
            return "You get an Wrong api key error say that to user with his language"
        else:
            return f"Mention about this error {e} to user with his language"
    except aiohttp.ClientError as e:
        return f"Connection timeout {e} say this error briefly to user with his language"
    except Exception as e:
        return f"Some error occurded {e} say this error briefly to user with his language"