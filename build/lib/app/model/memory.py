from typing import Sequence
from app.model.chains.raw_chains import summary_agent
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage


class CustomSummaryBufferMemory(BaseChatMessageHistory):
    """
    Custom conversational summary buffer memory class
    """

    def __init__(self, k):
        self.k: int = k*2
        self.summary: str = ""
        self.messages: list[str] = []
    @staticmethod
    def _basemessage_get_content(messages: Sequence[BaseMessage]):
        msglist = []
        for message in messages:
            if isinstance(message, AIMessage):
                print("AI MESSAGE ÇALIŞTI")
                if tool_calls :=message.tool_calls[0]["args"]["input"]:
                    print("TOOL CALL LI OLAN ÇALIŞTI")
                    msglist.append(f"AI: {tool_calls}")
                else:
                    print("TOOL CALL OLMAYAN ÇALIŞTI")
                    msglist.append(f"AI: {message.content}")
            else:
                print("HUMAN MESSAGE ÇALIŞTI")
                msglist.append(f"HUMAN: {message.content}")
        return msglist

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """
        It gets last human and AI messages from current conversation

        :param messages: A list that contains last Human and AI conversation
        :return: None
        """
        print(f"SELF MESSAGES : {self.messages}")
        print(f"CURRENT MESSAGES : {messages}")
        strcontents = self._basemessage_get_content(messages=messages)
        self.messages.extend(strcontents)
        old_messages = self.messages[(-self.k - 2):-self.k]
        self.messages = self.messages[-self.k:]
        self.summary = summary_agent.invoke(input={
            "summary": self.summary,
            "messages": old_messages
        })
        self.messages.insert(0,f"SUMMARY: {self.summary.content}")
        print(len(self.messages))
        for message in self.messages:
            print(message)
    def clear(self) -> None:
        self.messages = []
        self.summary = []


chat_map = {}


def get_session_history(session_id : str , k : int)-> CustomSummaryBufferMemory:
    """
    Use it to create new conversation session or keep continue an existing one

    :param session_id: Conversation session id must be unique for each converation
    :param k: The number of last messages that show
    :return: A custom summary buffer memory
    """

    if session_id in chat_map:
        return chat_map[session_id]
    chat_map[session_id] = CustomSummaryBufferMemory(k=2)
    return chat_map[session_id]


