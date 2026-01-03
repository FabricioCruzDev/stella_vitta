import asyncio
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.models.products import Product, ProductVariant, Price

async def seed_data():
    async with SessionLocal() as session:
        async with session.begin():
            # 1. Produto Exemplo
            p1 = Product(name="Colar Ponto de Luz", description="Zircônia premium com corrente veneziana")
            session.add(p1)
            await session.flush()

            # 2. Variantes (Ouro e Prata)
            v1 = ProductVariant(sku="COL-PL-OURO", finish="Ouro 18k", weight_grams=1.2, product_id=p1.id)
            v2 = ProductVariant(sku="COL-PL-PRATA", finish="Prata 925", weight_grams=1.1, product_id=p1.id)
            session.add_all([v1, v2])
            await session.flush()

            # 3. Preços (Atacado e Varejo)
            prices = [
                Price(variant_id=v1.id, price_type="retail", value=Decimal("120.00")),
                Price(variant_id=v1.id, price_type="wholesale", value=Decimal("60.00")),
                Price(variant_id=v2.id, price_type="retail", value=Decimal("95.00")),
                Price(variant_id=v2.id, price_type="wholesale", value=Decimal("47.50")),
            ]
            session.add_all(prices)
            
        print("✅ Banco de dados populado com sucesso!")

if __name__ == "__main__":
    asyncio.run(seed_data())