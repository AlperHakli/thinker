from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    AGENT_NAMES = [
        "MATH_AGENT",
        "CHAT_AGENT",
        "UTILITY_AGENT",
        "DATABASE_ANALYSIS_AGENT",
        "DATABASE_VISUALIZATION_AGENT"
    ]
    DATABASE_URL = os.getenv("DATABASE_URL")
    IP_API_URL = os.getenv("IP_API_URL")
    SERPAPI_API_KEY =os.getenv("SERPAPI_API_KEY")
    DESCRIBE_ATTRIBUTES = ["count", "mean", "standart_deviation", "minimum", "maximum"]
    DESCRIBE_DROP_ATTRIBUTES_LIST = ['25%', '50%', '75%']




settings = Settings()

