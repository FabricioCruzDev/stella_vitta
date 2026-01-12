from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.user import User, UserType
from app.schemas.user import UserCreate, UserRead, UserTypeCreate, UserTypeRead

router = APIRouter(prefix="/users", tags=["Users"])

## --- User Type ---
@router.post("/types", response_model=UserTypeRead, status_code=status.HTTP_201_CREATED)
async def create_user_type(type_data: UserTypeCreate, db: AsyncSession = Depends(get_db)):
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

## --- Create User ---
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Verifica duplicidade
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Este e-mail já foi cadastrado")

    # 2. Instancia o novo usuário
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=user_data.password, # Futuramente adicione a lógica de hash aqui
        user_type_id=user_data.user_type_id,
        role=user_data.role,
        is_active=True
    )

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        # 3. RECARREGA COM O RELACIONAMENTO (Evita o Erro 500)
        query_ref = select(User).options(selectinload(User.user_type)).where(User.id == new_user.id)
        result_ref = await db.execute(query_ref)
        return result_ref.scalar_one()
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

## --- Listagem e Dashboard ---
@router.get("/", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    query = select(User).options(selectinload(User.user_type))
    result = await db.execute(query)
    return result.scalars().all()

templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def user_dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    query = select(User).options(selectinload(User.user_type))
    result = await db.execute(query)
    users = result.scalars().all()

    return templates.TemplateResponse(
        "users_admin.html",
        {"request": request, "users": users}
    )

## --- Delete ---
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    await db.delete(user)
    await db.commit()
    return None