from datetime import datetime
from sqlalchemy.orm import registry, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, func, Integer, String, BigInteger, DateTime, Numeric

table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(30),unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, 
                                                 init=False, 
                                                 server_default=func.now(),
                                                 nullable=False)

    inventoryitem: Mapped[list['InventoryItem']] = relationship("InventoryItem",  
                                                                back_populates='user',
                                                                cascade='all, delete-orphan'
                                                                )
@table_registry.mapped_as_dataclass
class InventoryItem:
    __tablename__ = 'inventory_items'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    quantity: Mapped[float] = mapped_column(Numeric(10,2))
    unit: Mapped[str]= mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 init=False, 
                                                 server_default=func.now(), 
                                                 nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime,
                                                 init=False, 
                                                 server_default=func.now(),
                                                 onupdate= func.now(),
                                                 nullable=False)
    # image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    
    user: Mapped[User] = relationship("User", back_populates="inventory_items")