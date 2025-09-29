from typing import Union
from langchain_core.tools import tool
from app.model.db_cache import DB_CACHE


@tool
async def final_answer(
        cache_key: str,
        input: str = None,
) -> Union[dict, str]:
    """
    Use this tool to respond to user or agent

    <input> your output to show user you MUST FILL this with your response

    """
    # seneryolarım şunlar:
    # db analysis , db viz
    # db viz
    # db analysis
    try:
        if DB_CACHE[cache_key]["agent_counter"] == DB_CACHE[cache_key]["max_agent_count"]:
            print("INPUT RETURN WORKEDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
            return input  # final answer that show to user
        else:
            print("ANALYSIS RESULT RETURNED")
            return f"{DB_CACHE[cache_key]["analysis_result"]} call the next agent"  # internal answer of that agent to show forward agent
    except Exception as e:
        return f"call final_answer tool and summarize this error {e} briefly and give instructions about how to solve it "
