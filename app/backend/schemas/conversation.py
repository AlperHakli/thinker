from pydantic import BaseModel , Field


class Conversation(BaseModel):
    query : str = Field(... , title="User Query" , description="User message to AI")
    ai_response : str = Field(... , title="AI response" , description="Response of the AI")

