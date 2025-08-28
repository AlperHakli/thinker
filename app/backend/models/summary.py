from imports import *
from sqlalchemy import Integer,String,ForeignKey

class Summary(Base):
    conversation_id = Column(Integer ,
                             ForeignKey("conversation_table.conversation_id" , ondelete= "CASCADE"),
                             primary_key=True ,
                             unique= True ,
                             nullable= False,
                             )
    summary = Column(String)
