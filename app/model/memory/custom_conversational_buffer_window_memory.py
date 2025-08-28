from typing import Sequence
from app.model.chains.raw_chains import summary_agent
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage


class CustomConversationalSummaryBufferMemory(BaseChatMessageHistory):
    """
    Custom conversational summary buffer memory class
    """

    def __init__(self, k):
        self.k: int = k*2
        self.messages: list[str] = []
    @staticmethod
    def _basemessage_get_content(messages: Sequence[BaseMessage]):
        msglist = []
        for message in messages:
            if isinstance(message, AIMessage):
                msglist.append(f"AI: {message.tool_calls[0]["args"]["input"]}")
            else:
                msglist.append(f"HUMAN: {message.content}")
        return msglist

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """
        It gets last human and AI messages from current conversation

        :param messages: A list that contains last Human and AI conversation
        :return: None
        """
        strcontents = self._basemessage_get_content(messages=messages)
        self.messages.extend(strcontents)
        old_messages = self.messages[(-self.k - 2):-self.k]
        self.messages = self.messages[-self.k:]
        for message in self.messages:
            print(f"MESSAGE: {message}")
    def clear(self) -> None:
        self.messages = []


chat_map = {}


def get_session_history(session_id : str , k : int)-> CustomConversationalSummaryBufferMemory:
    """
    Use it to create new conversation session or keep continue an existing one

    :param session_id: Conversation session id must be unique for each converation
    :param k: The number of last messages that show
    :return: A custom summary buffer memory
    """

    if session_id in chat_map:
        return chat_map[session_id]
    chat_map[session_id] = CustomConversationalSummaryBufferMemory(k=2)
    return chat_map[session_id]


