from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(min_length=3)
    device_id: str
    
class UserCreate(UserBase):
    password: str = Field(min_length=4)
    
class User(UserBase):
    id: int
    password: str = Field(min_length=4)
    is_active: bool
    class Config:
        from_attributes = True

class SalesBase(BaseModel):
    year: int
    month: int = Field(ge=1, le=12)
    day: int = Field(ge=1, le=31)
    sales: int
    purchase: int
    income: int
    
class SalesCreate(SalesBase):
    pass

class Sales(SalesBase):
    sales_id: int
    user_id: int
    class Config:
        from_attributes = True
        
class MessageResponse(BaseModel):
    message: str