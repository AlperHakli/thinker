# from app.model.models import embedding_model
# from app.model.prompts import base_prompts
# from langchain_core.runnables import RunnableSerializable
# from langchain.tools import BaseTool
# from langchain_community.utils.math import cosine_similarity
# from app.model.utils.prompt_utils import prompt_to_str_converter
# from typing import List , Tuple
#
# #TODO Old embedding based agent router
# prompt_templates = [
#     base_prompts.math_agent_prompt,
#     base_prompts.chat_agent_prompt,
#     base_prompts.utility_agent_prompt,
#     base_prompts.database_analysis_agent_prompt,
#     base_prompts.database_visualization_agent_prompt,
# ]
#
# prompt_converted = prompt_to_str_converter(prompt_templates)
#
# prompt_embeddings = embedding_model.embed_documents(prompt_converted)
#
#
# def agent_router(
#                  embedded_input : list[float],
#                  agents_and_tools_list : List[Tuple[RunnableSerializable , List[BaseTool]]],
#                  prompt_embeddings: list[list[float]],
#                  agent_names:list[str] = None,
#                  verbose : bool = False
#
# )\
#         -> tuple[RunnableSerializable , list[BaseTool]]:
#     """
#     Agent router that works with OpenAI's embedding model it simply chose an agent based on user query
#
#     :param embedded_input: embedded user input
#     :param agents_and_tools_list: A list contains lists of agents and that agent's tools example = list[(agent1 , tool1) , (agen2 , tool2)]
#     :param prompt_embeddings: Prompt embedding of agents must have same sequence with agents_and_tools for example list[embedding1 , embedding2]
#     :param agent_names: Names of all agents to see which agent is running
#     :param verbose: To get dev information pass True if it is True then you must provide agent_names
#     :return: A tuple containing a RunnableSerializable object and a list of BaseTool objects, selected based on the user input.
#     """
#
#     similarity = cosine_similarity([embedded_input], prompt_embeddings)[0]
#     max_idx = similarity.argmax()
#     if verbose:
#         if agent_names:
#             print(f"Current Agent : {agent_names[max_idx]}")
#             print(f"Similarity Scores : {similarity}")
#     most_similar = agents_and_tools_list[max_idx]
#     return most_similar
#
#
#
#
