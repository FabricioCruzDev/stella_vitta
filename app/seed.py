import asyncio
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.models.products import Product, ProductVariant, Price
from app.models.user import User, UserType
from passlib.context import CryptContext

# Configuração para encriptar a senha do usuário de teste
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_data_product():
    async with SessionLocal() as session:
        async with session.begin():
            # --- 1. PRODUTOS ---
            p1 = Product(name="Colar Ponto de Luz", description="Zircônia premium")
            session.add(p1)
            await session.flush() # Gera o p1.id

            v1 = ProductVariant(sku="COL-PL-OURO", finish="Ouro 18k", weight_grams=1.2, product_id=p1.id)
            session.add(v1)
            await session.flush() # Gera o v1.id

            prices = [
                Price(variant_id=v1.id, price_type="retail", value=Decimal("120.00")),
                Price(variant_id=v1.id, price_type="wholesale", value=Decimal("60.00")),
            ]
            session.add_all(prices)
        print("✅ Banco populado: Produtos criados!")

async def seed_data_user():
    async with SessionLocal() as session:
        async with session.begin():
            # --- PASSO 1: Criar os Tipos de Usuário ---
            admin_type = UserType(name="admin", description="Admin")
            wholesale_type = UserType(name="wholesale", description="Revendedor")
            retail_type = UserType(name="retail", description="Cliente")
            
            session.add_all([admin_type, wholesale_type, retail_type])
            
            # --- PASSO 2:---
            # O flush força o SQLAlchemy a enviar os UserTypes para o banco
            # para que o Postgres gere os IDs (1, 2, 3), mas SEM fechar a transação.
            await session.flush() 

            # --- PASSO 3:---
            #  Criar o Usuário usando o ID gerado ---
            
            test_user = User(
                first_name="Fabrício",
                last_name="Mendes",
                email="revenda@stella.com",
                hashed_password='senha123',
                is_active=True,
                role="retail",
                user_type_id=wholesale_type.id # O ID já existe aqui graças ao flush!
            )
            session.add(test_user)
            
        # O commit acontece automaticamente ao sair do bloco 'async with session.begin()'
        print("✅ Usuário e tipos de usuário criados com sucesso!")

async def main():
    # Executa as duas tarefas em sequência dentro do mesmo loop
    #await seed_data_product()
    await seed_data_user()

if __name__ == "__main__":
    asyncio.run(main())