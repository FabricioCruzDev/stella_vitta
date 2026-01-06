from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User, UserType
from app.schemas.user import UserCreate, UserRead, UserTypeCreate, UserTypeRead


router = APIRouter(prefix="/users", tags=["Users"])


## User_type
@router.post("/types", response_model=UserTypeRead, status_code=status.HTTP_201_CREATED)
async def create_user_type(type_data: UserTypeCreate, db: AsyncSession = Depends(get_db)):
    # Verifica se já existe um tipo com esse nome
    query = select(UserType).where(UserType.name == type_data.name)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Este tipo de usuário já existe.")

    new_type = UserType(
        name=type_data.name,
        description=type_data.description
    )
    
    db.add(new_type)
    await db.commit()
    await db.refresh(new_type)
    return new_type

## User
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def  create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code = 400,
            detail = "Este e-mail já foi cadastrado"
        )
    
    new_user = User (
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        email = user_data.email,
        hashed_password= user_data.password,
        user_type_id = user_data.user_type_id,
        is_activate = True
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user