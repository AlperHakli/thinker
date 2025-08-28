from typing import Sequence
from app.model.chains.raw_chains import summary_agent
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage


class CustomConversationalSummaryBufferMemory(BaseChatMessageHistory):
    """
    Custom conversational summary buffer memory class\n
    Langchain's RunnableWithMessageHistory class will use add_messages function automatically \n
    It keeps last k number of messages and summarization of old messages in the self.messages variable

    :param k: Last number of messages that will add to self.messages more k value means more token usage



    """

    def __init__(self, k):
        self.k: int = k * 2
        self.summary: str = ""
        self.messages: list[str] = []

    @staticmethod
    def _basemessage_get_content(messages: Sequence[BaseMessage]) \
            -> list[str]:
        """
        It converts AIMessage and HumanMessage to string to  decrease token usage

        :param messages: Messages of user and AI
        :return: string converted messages list
        """
        msglist = []
        for message in messages:
            if isinstance(message, AIMessage):
                if message.tool_calls and message.tool_calls[0]["args"].get("input"):
                    msglist.append(f"AI: {message.tool_calls[0]['args']['input']}")
                else:
                    msglist.append(f"AI: {message.content}")
            else:
                msglist.append(f"HUMAN: {message.content}")
        return msglist

    def add_messages(self, messages: Sequence[BaseMessage])\
            -> None:
        """
        It gets last human and AI messages from current conversation

        :param messages: A list that contains last Human and AI conversation
        :return: None
        """
        self.messages = self.messages[1:]
        # print(f"SELF MESSAGES : {self.messages}")
        # print(f"MESSAGES : {messages}")
        strcontents = self._basemessage_get_content(messages=messages)
        # print(f"STRCONTENTS : {strcontents}")
        self.messages.extend(strcontents)
        old_messages = self.messages[(-self.k - 2):-self.k]
        self.messages = self.messages[-self.k:]
        self.summary = summary_agent.invoke(input={
            "summary": self.summary,
            "messages": old_messages
        })
        # print(f"CONTENT : {self.summary.content}")
        self.messages.insert(0, f"SUMMARY: {self.summary.content}")
        for message in self.messages:
            print(f"MESSAGE: {message}")

    def clear(self) -> None:
        self.messages = []
        self.summary = []


chat_map = {}


def get_session_history(session_id: str, k: int) -> CustomConversationalSummaryBufferMemory:
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
