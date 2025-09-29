from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from app.config import settings
from langchain_core.runnables import ConfigurableField
from langchain_core.runnables import RunnableSerializable

model_name = "gpt-4.1-nano"

embedding_model_name = "text-embedding-3-small"

embedding_model = OpenAIEmbeddings(model=embedding_model_name, api_key=settings.OPENAI_API_KEY)


def model_creator(
        temperature: float
) \
        -> RunnableSerializable:
    """
    Actuallty this Doesn't necessary I wrote this only to prevent repeating same code :)

    :param temperature: temperature value closer to 1 mean model hallucinate more
    :return: Gpt 4.1-nano model RunnableSerializable
    """
    return ChatOpenAI(
        model=model_name,
        streaming=True,
        api_key=settings.OPENAI_API_KEY,
        temperature=temperature
        # Model will use this callback every time when it creates new token
    ).configurable_fields(callbacks=ConfigurableField(
        name="callbacks",
        id="callbacks",
        description="list of callbacks"
    ))


chat_model = model_creator(temperature=0.7)

utility_model = model_creator(temperature=0)

summarymodel = ChatOpenAI(
    model=model_name,
    api_key=settings.OPENAI_API_KEY,
)
