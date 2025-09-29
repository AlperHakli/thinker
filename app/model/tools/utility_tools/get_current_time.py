import datetime
import pytz
from langchain_core.tools import tool
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