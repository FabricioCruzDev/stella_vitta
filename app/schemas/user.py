from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

#Identifica usuário
class UserTypeRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes = True)

#Criação
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role: str
    user_type_id: int

#Retorno 
class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    user_type_id: int
    user_type: UserTypeRead

    model_config = ConfigDict(from_attributes = True)

#Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#Criação
class UserTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None

#Retorno
class UserTypeRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)