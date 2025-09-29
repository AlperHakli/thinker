from requests.exceptions import ConnectTimeout , Timeout
from langchain_core.tools import tool
import httpx
from app.config import settings
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