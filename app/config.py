from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    # old agent router parameters
    # AGENT_NAMES = [
    #     # "MATH_AGENT",
    #     "CHAT_AGENT",
    #     # "UTILITY_AGENT",
    #     "DATABASE_ANALYSIS_AGENT",
    #     "DATABASE_VISUALIZATION_AGENT"
    # ]

    DATABASE_URL = os.getenv("DATABASE_URL")
    IP_API_URL = os.getenv("IP_API_URL")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    VISUALIZATION_SIZE = (4, 3)  # default: (4,3)


settings = Settings()
