from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_deviceId(db: Session, device_id: str):
    return db.query(models.User).filter(models.User.device_id == device_id).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_username_and_pass(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user and pwd_context.verify(password, user.password):
        return user
    return None     
    
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password, device_id=user.device_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
def get_sales(db: Session, user_id: int):
    return db.query(models.Sales).filter(models.Sales.user_id == user_id).all()

def get_sales_by_year(db: Session, year: int):
    return db.query(models.Sales).filter(models.Sales.year == year).all()

def create_sales(db: Session, sales: schemas.SalesCreate, user_id: int):
    db_sales = models.Sales(
        income = sales.income,
        sales = sales.sales, 
        purchase = sales.purchase,
        year = sales.year,
        month = sales.month,
        day = sales.day,
        user_id = user_id
    )
    db.add(db_sales)
    db.commit()
    db.refresh(db_sales)
    return db_sales

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True  # 削除が成功した場合は True を返す
    return False  # ユーザーが見つからなかった場合は False を返す