from langchain_core.prompts import ChatPromptTemplate


def prompt_to_str_converter(prompts: list[ChatPromptTemplate]) \
        -> list[str]:
    """
    :param prompts: list of the prompts
    :return: The plain text content of the first and primary SystemMessagePromptTemplate
    """
    converted_list = [prompt[0].prompt.template for prompt in prompts]
    return converted_list
