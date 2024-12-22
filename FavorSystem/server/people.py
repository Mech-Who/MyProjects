from datetime import datetime
from typing import List, Tuple, Dict, Iterable, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlmodel import Session, SQLModel, create_engine, select, delete, update

from config import ReadConfig
from entity import People, PeopleParam, Event
from database import engine, create_db_and_tables

create_db_and_tables()

config = ReadConfig()
people_api = FastAPI()

"""
Query Form
"""

class PageQuery(BaseModel):
    page_size: int # 一页有多少条
    page_num: int   # 第几页

class PeopleCreateQuery(BaseModel):
    id: int|None = Field(default=None)
    name: str|None = Field(default=None)
    birthday: str|None = Field(default=None)
    gender: int|None = Field(default=None)
    favor: float|None = Field(default=None)

class PeopleDeleteQuery(BaseModel):
    id: int|None = Field(default=None)

class PeopleUpdateQuery(BaseModel):
    id: int|None = Field(default=None)
    name: str|None = Field(default=None)
    birthday: str|None = Field(default=None)
    startDate: str|None = Field(default=None)
    endDate: str|None = Field(default=None)
    gender: int|None = Field(default=None)
    favor: float|None = Field(default=None)

class PeopleInfoQuery(BaseModel):
    id: int|None = Field(default=None)
    name: str|None = Field(default=None)
    birthday: str|None = Field(default=None)
    gender: int|None = Field(default=None)
    favor: float|None = Field(default=None)

"""
People
"""

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
def create_people(people_list: List[PeopleCreateQuery]):
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
def delete_people(people_list: List[PeopleDeleteQuery]):
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

@people_api.post("/update")
def update_people(people_list: List[PeopleUpdateQuery]):
    with Session(engine) as session:
        for people in people_list:
            statement = update(People).where(People.id == people["id"])
            if people.id:
                statement.values(id=people.id)
            # TBD: 其他属性
            update_count = session.exec(statement).first()
        session.commit()
    print(f"[INFO] Update {len(people_list)} people.")
    return { "status": 200 }

@people_api.post("/get_info")
def get_people_info(people: PeopleInfoQuery):
    with Session(engine) as session:
        statement = select(People).where(People.removed == 0)
        if people.id:
            statement = statement.where(People.id == people.id)
        if people.name:
            statement = statement.where(People.name == people.name)
        if people.birthday:
            statement = statement.where(People.birthday == people.birthday)
        if people.favor:
            statement = statement.where(People.favor == people.favor)
        people_info = session.exec(statement).first()
        # 非空查询则event
        if people_info:
            statement = select(Event).where(Event.removed == 0)\
                        .where(Event.owner_id == people_info.id)
            events = session.exec(statement).all()
    result = { key: value for key, value in people_info.model_dump().items() if key != "removed"}
    result["latest_event"] = [{key: value for key, value in event.model_dump().items() if key != "removed"} for event in events]
    # 以下三种方式均可
    return result # 纯dict，自定义更方便
    # return people_info # 纯BaseModel
    # return { **people_info.model_dump(), "latest_event": events } # 半BaseModel，半dict

"""
People Param
"""

@people_api.post("/add_param")
def add_people_param():
    pass

@people_api.post("/modify_param")
def modify_people_param():
    pass

@people_api.post("/remove_param")
def remove_people_param():
    pass

