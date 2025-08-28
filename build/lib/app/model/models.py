from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from config import settings
from langchain_core.runnables import ConfigurableField

model_name = "gpt-4.1-nano"

embedding_model_name = "text-embedding-3-small"

embedding_model = OpenAIEmbeddings(model=embedding_model_name, api_key=settings.OPENAI_API_KEY)


basemodel = ChatOpenAI(
    model=model_name,
    streaming=True,
    api_key=settings.OPENAI_API_KEY,
).configurable_fields(callbacks=ConfigurableField(
    name="callbacks",
    id="callbacks",
    description="list of callbacks"
))

summarymodel = ChatOpenAI(
    model = model_name,
    api_key = settings.OPENAI_API_KEY,
)


