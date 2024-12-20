from datetime import datetime
from typing import List, Tuple, Dict, Iterable, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlmodel import Session, SQLModel, create_engine, select, delete, update

from config import ReadConfig
from entity import People, PeopleParam
from database import engine, create_db_and_tables

create_db_and_tables()

config = ReadConfig()
people_api = FastAPI()

@people_api.get("/")
def list_all_people():
    with Session(engine) as session:
        statement = select(People).limit(20)
        peoples = session.exec(statement).all()
        print(peoples)
        return { "people_list": peoples }

@people_api.post("/create")
def create_people(people_list: List[Dict]):
    """
    add a bunch of people to database
    """
    with Session(engine) as session:
        p_list = []
        for people in people_list:
            p = People(name=people["name"],
                       birthday=datetime.strptime(people["birthday"], config["date_format"]),
                       gender=people["gender"],
                       favor=people["favor"])
            p_list.append(p)
            session.add(p)
        session.commit()
        for p in p_list:
            session.refresh(p)
        people_count = len(people_list)
        suffix = 's' if people_count > 1 else ''
        print(f"[INFO] Create {people_count} people{suffix}.")
        return { "status": 200 }

@people_api.post("/delete")
def delete_people(id_list):
    with Session(engine) as session:
        for id in id_list:
            statement = delete(People).where(People.id == id)
            people_count = session.exec(statement).first()
        session.commit()
        people_count = len(id_list)
        suffix = "s" if people_count > 1 else ""
        print(f"[INFO] Delete {len(id_list)} people{suffix}.")
        return { "status": 200 }

@people_api.post("/modify")
def modify_people(people_list):
    with Session(engine) as session:
        for people in people_list:
            statement = update(People).where(People.id == people["id"])
            update_count = session.exec(statement).first()
        session.commit()
    print(f"[INFO] Update {len(people_list)} people.")
    return { "status": 200 }

@people_api.post("/add_param")
def add_people_param():
    pass

@people_api.post("/modify_param")
def modify_people_param():
    pass

@people_api.post("/remove_param")
def remove_people_param():
    pass

@people_api.post("/list")
def list_people(id=None, name=None,
                start_birthday=None,
                end_birthday=None,
                gender=None, favor=None):
    with Session(engine) as session:
        statement = select(People)
        if id:
            statement = statement.where(People.id == id)
        if name:
            statement = statement.where(People.name == name)
        if start_birthday:
            start = datetime.strptime(start_birthday, config["date_format"])
            statement = statement.where(People.birthday > start)
        if end_birthday:
            end = datetime.strptime(end_birthday, config["date_format"])
            statement = statement.where(People.birthday < end)
        if gender:
            statement = statement.where(People.gender == gender)
        if favor:
            statement = statement.where(People.favor == favor)
        peoples = session.exec(statement).all()
        print(peoples)
    return { "people_list": peoples }
