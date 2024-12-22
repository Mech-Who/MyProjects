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

class PageQuery(BaseModel):
    page_size: int # 一页有多少条
    page_num: int   # 第几页

@people_api.post("/list")
def list_people(page: PageQuery):
    print(f"{page.page_size=}, {page.page_num=}")
    total_count = people_count()
    total_page = total_count / page.page_size
    with Session(engine) as session:
        statement = select(People).where(People.removed == 0)\
            .offset(page.page_size*page.page_num).limit(page.page_size)
        peoples = session.exec(statement).all()
        print(peoples)
        return {
            "people_list": peoples,
            "total_page": total_page,
            "current_page": page.page_num,
            "total_count": total_count,
        }

def people_count():
    people_count = 0
    with Session(engine) as session:
        statement = select(People)
        peoples = session.exec(statement).all()
        people_count = len(peoples)
    return people_count

@people_api.post("/create")
def create_people(people_list: List[People]):
    """
    add a bunch of people to database
    """
    people_count = len(people_list)
    print(people_list)
    with Session(engine) as session:
        p_list = []
        for people in people_list:
            p = People(name=people.name,
                       birthday=datetime.strptime(people.birthday, config["date_format"]),
                       gender=people.gender,
                       favor=people.favor)
            p_list.append(p)
            session.add(p)
        session.commit()
        for p in p_list:
            session.refresh(p)
    suffix = 's' if people_count > 1 else ''
    print(f"[INFO] Create {people_count} people{suffix}.")
    return { "status": 200 }

@people_api.post("/delete")
def delete_people(people_list: List[People]):
    with Session(engine) as session:
        for people in people_list:
            # 真的删除
            # statement = delete(People).where(People.id == people.id)
            # 修改标记式删除，这种更好，可以找回
            statement = update(People).where(People.id == people.id)\
                        .values(removed=1)
            people_count = session.exec(statement)
        session.commit()
        people_count = len(people_list)
        suffix = "s" if people_count > 1 else ""
        print(f"[INFO] Delete {len(people_list)} people{suffix}.")
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

