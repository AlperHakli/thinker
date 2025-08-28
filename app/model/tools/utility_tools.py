import asyncio
import datetime
from typing import Union
import serpapi
from langchain_community.utilities import SerpAPIWrapper
import pytz
from langchain_core.tools import tool
from requests.exceptions import Timeout, ConnectionError, ConnectTimeout
from config import settings
import httpx
import aiohttp


@tool
async def get_location() \
        -> dict:
    """Use it to get current location returns country name , city name , timezone , latitude and longitude"""
    try:
        async with httpx.AsyncClient() as client:
            result = await client.get(url=settings.IP_API_URL, timeout=10.0)
            result = result.json()
            return {
                "country": result.get("country"),
                "city": result.get("city"),
                "timezone": result.get("timezone"),
                "lat": result.get("lat"),
                "lon": result.get("lon")
            }
    except ConnectTimeout as c:
        print(f"Server connection time out : {c}")
    except Timeout as t:
        print(f"General time out error (probably when fetching the data from server) : {t}")
    except ConnectionError as c:
        print(f"Connection error check your internet connection")
    except Exception as e:
        print(f"Unknown exception occurded {e}")


@tool
async def get_current_time(timezone: str = None) \
        -> str:
    """
    If user wants to learn current date , year , month etc. use this tool
    Example triggers : 'what time is it' , 'what year is it' etc.
    """
    if timezone is None:
        time = datetime.datetime.now()
        return time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        try:
            timezone = pytz.timezone(timezone)
            time = datetime.datetime.now(tz=timezone)
            return time.strftime("%Y-%m-%d %H:%M:%S")
        except pytz.exceptions.UnknownTimeZoneError:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
            return e
    except aiohttp.ClientError as e:
        return f"Connection timeout {e} say this error briefly to user with his language"
    except Exception as e:
        return f"Some error occurded {e} say this error briefly to user with his language"
