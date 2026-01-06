from sqlalchemy import Column, String, ForeignKey, Numeric, Boolean, Integer
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    variants = relationship("ProductVariant", back_populates="product")


class ProductVariant(Base):
    __tablename__ = "product_variants"
    id = Column(Integer, primary_key=True)
    sku = Column(String, nullable=False, unique=True)
    finish = Column(String) #AG OU AU
    weight_grams = Column(Numeric)
    product_id = Column(Integer, ForeignKey("product.id"))

    product = relationship("Product", back_populates="variants")
    price = relationship("Price", back_populates="variant")


class Price(Base):
    __tablename__ = "price"
    id = Column(Integer, primary_key=True)
    variant_id = Column(Integer, ForeignKey('product_variants.id'))
    price_type = Column(String, nullable=False) # 'retail' ou 'wholesale'
    value = Column(Numeric(10, 2), nullable=False)

    variant = relationship("ProductVariant", back_populates="price")