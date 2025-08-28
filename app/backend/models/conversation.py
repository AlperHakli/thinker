from imports import *
from sqlalchemy import Integer, String , ForeignKey
from sqlalchemy.orm import relationship


class Conversation(Base):
    __tablename__ = "conversation_table"
    conversation_id = Column(Integer, primary_key=True, unique=True , autoincrement= True , nullable= False)
    user_id = Column(Integer , ForeignKey("user_table.user_id" , ondelete="CASCADE") , nullable= False)
    ai_message = Column(String)
    user_message = Column(String)
    conversation_user_relationship = (
        relationship("User",
                     back_populates="user_conversation_relationship",
                     foreign_keys=user_id,
                     ))
