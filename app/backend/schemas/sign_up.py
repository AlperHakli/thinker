from pydantic import BaseModel , Field


class SignUp(BaseModel):
    username: str = Field(... , title= "Username" , description="Username of the user")
    email: str = Field(... , title="Email" , description="Email of the user")
    password: str = Field(... , title= "Password" , description="Password of the user")

class SignIn(BaseModel):
    username: str = Field(... , title= "Username" , description="Name of the user that will use to sign in")
    password: str = Field(..., title="Password", description="Password of the user that will use to sign in")

class ChangePassword(BaseModel):
    old_password: str = Field(... , title="Old_password" , description="Old password of the user")
    new_password: str = Field(... , title="New_password" , description="New password to change")

class SignUpResponse(BaseModel):
    id : int = Field(... , title="user_ID" , description="ID of the user")
    username: str = Field(..., title="Username", description="Username of the user")
    email: str = Field(..., title="Username", description="Email of the user")
