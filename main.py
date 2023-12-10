from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime




DATABASE_URL = "sqlite:///./sos.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "device_data"
    id = Column(Integer, primary_key=True, index=True)
    dev_id = Column(Integer, index=True)
    sec_id = Column(Integer, index=True)
    sec_location = Column(String)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
class users(Base):
    __tablename__ = "User_data"
    id = Column(Integer, primary_key=True, index=True)
    dev_id = Column(Integer, index=True)
    User_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)


class createuser(BaseModel):
    dev_id: int
    User_name: str


class responseuser(BaseModel):
    id: int
    dev_id: int
    User_name: str
    created_at: datetime

class alertdata(BaseModel):
    id: int
    dev_id: int
    sec_id: int
    sec_location: str
    message: str
    created_at: datetime

class alertdetail(BaseModel):
    id: int
    dev_id: int
    sec_id: int
    sec_location: str
    message: str
    User_name:str
    created_at: datetime

class ItemCreate(BaseModel):
    dev_id: int
    sec_id: int
    sec_location: str
    message: str


# FastAPI app
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/alertdata/", response_model=alertdata)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.post("/createuser/", response_model=responseuser)
def create_item(user: createuser, db: Session = Depends(get_db)):
    db_item = users(**user.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/alertid/{item_id}", response_model=alertdata)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="No alert found in given id")
    return db_item

@app.get("/last_alert" ,response_model=alertdetail)
def get_last_inserted_row(db: Session = Depends(get_db)):
    last_row = db.query(Item).order_by(Item.id.desc()).first()
    db_device =db.query(users).filter(users.dev_id == last_row.dev_id).first()
    if db_device is not None:
        last_row.User_name = db_device.User_name
    else:
        last_row.User_name = "no username"
    if last_row is None:
        raise HTTPException(status_code=404, detail="No alerts found")
    return last_row



def lastalert(db: Session):
    last_row = db.query(Item).order_by(Item.id.desc()).first()
    print("Last alert created_at:", last_row.created_at)
    last_row.User_name = "no username"
    current_utc_time = datetime.utcnow()
    if last_row.created_at.hour == current_utc_time.hour and last_row.created_at.minute == current_utc_time.minute:
        return last_row
    else:
        return {"message":"No Alerts"}



# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=80)