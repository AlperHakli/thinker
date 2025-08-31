from app.model.chains import raw_chains
from langchain_core.runnables import RunnableSerializable, ConfigurableFieldSpec, RunnableWithMessageHistory
from app.model.memory import custom_conversational_buffer_window_memory, custom_conversational_summary_buffer_memory
from langchain_core.chat_history import BaseChatMessageHistory


def summary_buffer_memory_maker(
                runnable: RunnableSerializable,
        ):
    return (
        RunnableWithMessageHistory(
            runnable=runnable,
            input_messages_key="query",
            history_messages_key="memory",
            get_session_history=custom_conversational_summary_buffer_memory.get_session_history,
            history_factory_config=[
                ConfigurableFieldSpec(
                    name="k",
                    id="k",
                    description="last number of messages that show",
                    default=3,
                    annotation=int
                ),
                ConfigurableFieldSpec(
                    name="session_id",
                    id="session_id",
                    description="conversation session id (must be unique for each conversation)",
                    default="id123",
                    annotation=str
                )

            ]))

def buffer_window_memory_maker(
        runnable : RunnableSerializable
):
    return (
        RunnableWithMessageHistory(
            runnable=runnable,
            input_messages_key="query",
            history_messages_key="memory",
            get_session_history=custom_conversational_buffer_window_memory.get_session_history,
            history_factory_config=[
                ConfigurableFieldSpec(
                    name="k",
                    id="k",
                    description="last number of messages that show",
                    default=3,
                    annotation=int
                ),
                ConfigurableFieldSpec(
                    name="session_id",
                    id="session_id",
                    description="conversation session id (must be unique for each conversation)",
                    default="id123",
                    annotation=str
                )

            ]))


math_agent_with_memory = summary_buffer_memory_maker(raw_chains.math_agent)
chat_agent_with_memory = summary_buffer_memory_maker(raw_chains.chat_agent)
utility_agent_with_memory = summary_buffer_memory_maker(raw_chains.utility_model)
data_analysis_agent_with_memory = summary_buffer_memory_maker(raw_chains.data_analysis_agent)

