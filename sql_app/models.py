from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    
class Sales(Base):
    __tablename__ = "sales"
    sales_id = Column(Integer, primary_key=True) 
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False, index=True)
    income = Column(Integer)
    sales = Column(Integer) 
    purchase = Column(Integer) 
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)