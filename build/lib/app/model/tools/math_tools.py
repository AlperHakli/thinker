from langchain_core.tools import tool


@tool
async def arithmetic_calculations(problem: str)\
        -> float:
    """
    Use this when you want to calculate arithmetic problems
    If problem doesn't contain number then do not use this.
    """
    problem = problem.replace("^", "**")
    result = eval(problem)
    return result
