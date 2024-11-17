from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already register")
    return crud.create_user(db=db, user=user)

@app.get("/users/auth", response_model=schemas.User)
def auth_user(username: str, password: str, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_username_and_pass(db, username=username, password=password)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user

@app.get("/users/deviceId", response_model=schemas.User)
def get_deviceId(deviceId: str, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_deviceId(db, device_id=deviceId)
    if db_user is None:
        raise HTTPException(status_code=404, detail="device id not found")
    return db_user
    
@app.post("/sales/", response_model=schemas.Sales)
def create_sales(sales: schemas.SalesCreate, user_id: int, db: Session=Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return crud.create_sales(db=db, sales=sales, user_id=db_user.id)

@app.get("/sales/", response_model=list[schemas.Sales])
def get_sales(user_id: int, db: Session=Depends(get_db)):
    sales = crud.get_sales(db=db, user_id=user_id)
    return sales

@app.put("/users/{device_id}")
def update_active(device_id: str, is_active: bool, db: Session = Depends(get_db)):
    user = crud.update_user_active(db=db, device_id=device_id, is_active=is_active)
    if user:
        return {"message": "User authentication status updated successfully.", "user": user}
    return {"message": "User not found."}, 404

@app.delete("/users/{user_id}", response_model=schemas.MessageResponse)
def deleteUser(user_id: int, db: Session=Depends(get_db)):
    success = crud.delete_user(db=db, user_id=user_id)
    if success:
        return {"message": "User deleted successfully."}
    return {"message": "User not found."}, 404