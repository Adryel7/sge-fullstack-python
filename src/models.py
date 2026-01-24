from typing import Optional, List
from datetime import date
from sqlalchemy import String, Integer, ForeignKey, Text, Date, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Classe base para todos os modelos
class Base(DeclarativeBase):
    pass

class Department(Base):
    __tablename__ = "departments"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relacionamento: Um departamento pode ter vários representantes
    representatives: Mapped[List["Representative"]] = relationship(back_populates="department")

class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relacionamento: Uma categoria pode ter vários produtos
    products: Mapped[List["Product"]] = relationship(back_populates="category")

class Representative(Base):
    __tablename__ = "representatives"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    department: Mapped["Department"] = relationship(back_populates="representatives")

class InventoryManager(Base):
    __tablename__ = "inventory_managers"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    min_balance: Mapped[int] = mapped_column(Integer, default=0)
    quantity_in_stock: Mapped[int] = mapped_column(Integer, default=0)

    category: Mapped["Category"] = relationship(back_populates="products")

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # 'Entrada' ou 'Saída'
    type: Mapped[str] = mapped_column(String(3), nullable=False) 
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    representative_id: Mapped[int] = mapped_column(ForeignKey("representatives.id"))
    inventory_manager_id: Mapped[int] = mapped_column(ForeignKey("inventory_managers.id"))
    obs: Mapped[Optional[str]] = mapped_column(Text)

    # Restrição para garantir que o tipo seja apenas Entrada ou Saída (Check Constraint)
    __table_args__ = (
        CheckConstraint(type.in_(['IN', 'OUT']), name='check_transaction_type'),
    )