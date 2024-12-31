from pydantic import BaseModel, ConfigDict, EmailStr

class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ItemSchema(BaseModel):
    name: str
    description: str | None = None
    location: str | None = None
    quantity: float 
    unit: str


class ItemPublic(ItemSchema):
    id: int

class ItemList(BaseModel):
    items: list[ItemPublic]

class ItemUpdate(BaseModel):
    name: str
    description: str | None
    location: str | None
    quantity: float 
    unit: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


class FilterItem(FilterPage):
    name: str
    quantity: float 
    location: str | None 
    description: str | None 