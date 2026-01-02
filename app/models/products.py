from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class PriceType(enum.Enum):
    RETAIL = "retail"
    WHOLESALE = "wholesale"


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    variants = relationship("ProductVariant", back_populates="product")


class ProductVariant(Base):
    __tablename__ = "product_variants"
    id = Column(Integer, primary_key=True)
    sku = Column(Integer, unique=True)
    finish = Column(String) #AG OU AU
    product_id = Column(Integer, ForeignKey("product.id"))

    product = relationship("Product", back_populates="variants")
    prices = relationship("Price", back_populates="variant")


class Price(Base):
    __tablename__ = "price"
    id = Column(Integer, primary_key=True)
    variant_id = Column(Integer, ForeignKey('product_variants.id'))
    price_type = Column(Enum(PriceType))
    value = Column(Numeric(10,2))

    variant = relationship("ProductVariant", back_populates="price")