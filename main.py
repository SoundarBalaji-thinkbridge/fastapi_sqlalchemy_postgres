import csv
import json

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def json_values(csvfilepath=r'UsersData.csv', db: Session = Depends(get_db)):
    data = {}
    with open(csvfilepath, encoding='utf-8') as csvfh:
        csvreader = csv.DictReader(csvfh)
        for rows in csvreader:
            key = int(rows['ID'])
            data[key] = rows

    return data


@app.get('/')
async def json_display(json1=Depends(json_values)):
    jsonvalues = json.dumps(json1)
    jsonvaluesloaded = json.loads(jsonvalues)
    return jsonvaluesloaded


@app.get('/post/')
async def sendtodb(json1=Depends(json_values), db: Session = Depends(get_db)):
    for i in json1:
        name = json1[i]["Name"]
        email = json1[i]["MailID"]
        db_user = models.User(email=email, name=name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user


# @app.post('/send/', response_model=schemas.User)
# async def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
#     db_user = models.User(email=user.email, name=user.name)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


@app.get('/db/', response_model=List[schemas.User])
async def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).offset(0).limit(100).all()
