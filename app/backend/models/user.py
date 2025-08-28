from imports import *
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import relationship
from app.backend.user_roles import UserRoles


class User(Base):
    __tablename__ = "user_table"
    user_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    username = Column(String)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(Enum(UserRoles))
    user_conversation_relationship = relationship(
        "Conversation",
        back_populates="conversation_user_relationship",
        foreign_keys="conversation_table.user_id")
