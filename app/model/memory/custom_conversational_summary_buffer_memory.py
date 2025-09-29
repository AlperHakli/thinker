from typing import Sequence
from app.model.chains.raw_chains import summary_agent
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage
import streamlit as st

counter = 1
class CustomConversationalSummaryBufferMemory(BaseChatMessageHistory):
    """
    Custom conversational summary buffer memory class\n
    Since the langchain's ConversationSummaryBufferMemory class deprecated I built a custom memory class\n
    It keeps last k*2 number of messages and summary of old messages\n
    Thanks to James Briggs for teaching me this\n
    Langchain's RunnableWithMessageHistory class will use add_messages function automatically\n
    James Briggs's Tutorial : https://www.youtube.com/watch?v=Cyv-dgv80kE&t=16425s&ab_channel=JamesBriggs\n
    Langchain's ConversationSummaryBufferMemory document : https://python.langchain.com/api_reference/langchain/memory/langchain.memory.summary_buffer.ConversationSummaryBufferMemory.html

    :param k: last number of messages
    """

    def __init__(self, k):
        self.k: int = k * 2
        self.summary: AIMessage = AIMessage(content="")
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
        It adds new 2 messages to main message list (self.messages) and summarize the old messages\n
        and add that summarization to main summarization
        It works like this:
            Suppose we have messages: 1, 2, 3, 4 and k = 2 (meaning we keep last k*2 messages)\n
          - Step 1 self messages = [empty,1,2,3,4]
          - Step 2 self messages = [empty,1,2,3,4,5,6]
          - Step 3 old messages = [1,2] and self messages = [3,4,5,6] and self summary equals summary of old messages + current summary (which is empty in first step)
          - Step 4 self messages = [self summary,3,4,5,6]

        Langchain will use last self messages in the every conversation

        :param messages: A list that contains last Human and AI conversation
        :return: None
        """
        # Prevents adding user and AI messages to memory on every invoke, except when invoking last agent's final_answer.
        for msg in messages:
            if isinstance(msg , AIMessage) and msg.tool_calls and st.session_state["last_agent_seen"]:
                tool_name = msg.tool_calls[0]["name"]
                if tool_name != "final_answer":
                    print("SKİPPED MEMORY UPDATE")
                    return
        global counter
        print(f"ADD MESSAGES WORKED : {counter}")
        counter +=1
        self.messages = self.messages[1:]
        # print(f"SELF MESSAGES : {self.messages}")
        # print(f"MESSAGES : {messages}")
        strcontents = self._basemessage_get_content(messages=messages)
        # print(f"STRCONTENTS : {strcontents}")
        self.messages.extend(strcontents)
        old_messages = self.messages[(-self.k - 2):-self.k]
        self.messages = self.messages[-self.k:]
        self.summary = summary_agent.invoke(input={
            "summary": self.summary.content,
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
    Langchain's RunnableWithMessageHistory class will use this function to get the custom memory class

    :param session_id: Conversation session id must be unique for each conversation
    :param k: The number of last messages that will show
    :return: A custom summary buffer memory
    """

    if session_id in chat_map:
        return chat_map[session_id]
    chat_map[session_id] = CustomConversationalSummaryBufferMemory(k=2)
    return chat_map[session_id]
