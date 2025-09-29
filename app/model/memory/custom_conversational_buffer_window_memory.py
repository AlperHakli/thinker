from typing import Sequence
from app.model.chains.raw_chains import summary_agent
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage
counter = 1

class CustomConversationalBufferWindowMemory(BaseChatMessageHistory):
    """
    Custom conversational buffer window memory class\n
    Since the langchain's ConversationSummaryBufferMemory class deprecated I built a custom memory class\n
    It keeps only last k*2 number of messages
    Thanks to James Briggs for teaching me this\n
    Langchain's RunnableWithMessageHistory class will use add_messages function automatically\n
    James Briggs's Tutorial : https://www.youtube.com/watch?v=Cyv-dgv80kE&t=16425s&ab_channel=JamesBriggs\n
    Langchain's ConversationBufferWindowMemory document : https://python.langchain.com/api_reference/langchain/memory/langchain.memory.buffer_window.ConversationBufferWindowMemory.html

    :param k: last number of messages
    """

    def __init__(self, k):
        self.k: int = k*2
        self.messages: list[str] = []
    @staticmethod
    def _basemessage_get_content(messages: Sequence[BaseMessage])\
            -> list[str]:
        """
        It converts BaseMessage object to string and cleans the metadata to optimize tool usage

        :param messages: List of AIMessage and HumanMessage
        :return: List of strings that converted from BaseMessage list
        """
        msglist = []
        for message in messages:
            if isinstance(message, AIMessage):
                msglist.append(f"AI: {message.tool_calls[0]["args"]["input"]}")
            else:
                msglist.append(f"HUMAN: {message.content}")
        return msglist

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """
        It adds new 2 messages to main message list (self.messages) and cleans the last 2 messages
        It works like this:
            Suppose we have messages: 1, 2, 3, 4 and k = 2 (meaning we keep last k*2 messages)\n
          - Step 1 self messages = [1,2,3,4]
          - Step 2 self messages = [3,4,5,6] (message 1 and message 2 cleaned)

        Langchain will use last self messages in the every conversation

        :param messages: A list that contains last Human and AI conversation
        :return: None
        """
        # Prevents adding user and AI messages to memory on every invoke, except when invoking final_answer.
        for msg in messages:
            if isinstance(msg , AIMessage) and msg.tool_calls:
                tool_name = msg.tool_calls[0]["name"]
                if tool_name != "final_answer":
                    print("SKİPPED MEMORY UPDATE")
                    return
        global counter
        print(f"ADD MESSAGES WORKED : {counter}")
        counter +=1
        strcontents = self._basemessage_get_content(messages=messages)
        self.messages.extend(strcontents)
        old_messages = self.messages[(-self.k - 2):-self.k]
        self.messages = self.messages[-self.k:]
        for message in self.messages:
            print(f"MESSAGE: {message}")
    def clear(self) -> None:
        self.messages = []


chat_map = {}


def get_session_history(session_id : str , k : int)-> CustomConversationalBufferWindowMemory:
    """
    Langchain's RunnableWithMessageHistory class will use this function to get the custom memory class


    :param session_id: Conversation session id must be unique for each conversation
    :param k: The number of last messages that will show
    :return: A custom summary buffer memory
    """

    if session_id in chat_map:
        return chat_map[session_id]
    chat_map[session_id] = CustomConversationalBufferWindowMemory(k=2)
    return chat_map[session_id]


