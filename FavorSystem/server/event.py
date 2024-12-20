from datetime import datetime
from typing import List, Tuple, Dict, Iterable, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlmodel import Session, SQLModel, create_engine, select, delete, update

from config import ReadConfig
from entity import Event, EventParam
from database import engine, create_db_and_tables

create_db_and_tables()

config = ReadConfig()
event_api = FastAPI()

@event_api.get("/list_all")
def list_all_event(id=None, title=None,
                owner_id=None,
                related_people_id=None,
                related_event_id=None,
                start_date=None,
                end_date=None,
                description=None, favor_effect=None):
    with Session(engine) as session:
        statement = select(Event)
        if id:
            statement = statement.where(Event.id == id)
        if owner_id:
            statement = statement.where(Event.owner_id == owner_id)
        if title:
            statement = statement.where(Event.title == title)
        if start_date:
            start = datetime.strptime(start_date, config["date_format"])
            statement = statement.where(Event.event_date > start)
        if end_date:
            end = datetime.strptime(end_date, config["date_format"])
            statement = statement.where(Event.event_date < end)
        if description:
            statement = statement.where(Event.description in description)
        if favor_effect:
            statement = statement.where(Event.favor_effect == favor_effect)
        peoples = session.exec(statement).all()
        print(peoples)
    return { "people_list": peoples }

@event_api.post("/create")
def create_event(event_list: List[Dict]):
    """
    add a bunch of people to database
    """
    with Session(engine) as session:
        e_list = []
        for event in event_list:
            e = Event(owner_id=event["owner_id"],
                       event_date=datetime.strptime(event["event_date"], config["date_format"]),
                       title=event["title"],
                       description=event["title"],
                       favor_effect=event["favor"])
            e_list.append(e)
            session.add(e)
        session.commit()
        for e in e_list:
            session.refresh(e)
        event_count = len(event_list)
        suffix = 's' if event_count > 1 else ''
        print(f"[INFO] Create {event_count} event{suffix}.")
        return { "status": 200 }

@event_api.post("/delete")
def delete_event(id_list):
    with Session(engine) as session:
        for id in id_list:
            statement = delete(Event).where(Event.id == id)
            people_count = session.exec(statement).first()
        session.commit()
        event_count = len(id_list)
        suffix = 's' if event_count > 1 else ''
        print(f"[INFO] Delete {event_count} event{suffix}.")
        return { "status": 200 }

@event_api.post("/modify")
def modify_event(event_list):
    with Session(engine) as session:
        for event in event_list:
            statement = update(Event).where(Event.id == event["id"]) \
                        .values(owner_id=event["owner_id"],
                       event_date=datetime.strptime(event["event_date"], config["date_format"]),
                       title=event["title"],
                       description=event["title"],
                       favor_effect=event["favor"])
            update_count = session.exec(statement).first()
        session.commit()
    event_count = len(event_list)
    suffix = "s" if event_count > 1 else ""
    print(f"[INFO] Update {event_count} event{suffix}.")
    return { "status": 200 }

@event_api.post("/list")
def list_event():
    with Session(engine) as session:
        statement = select(Event).limit(20)
        events = session.exec(statement).all()
        print(events)
        return { "event_list": events }

@event_api.post("/add_related_people")
def add_related_people():
    pass

@event_api.post("/remove_related_people")
def remove_related_people():
    pass

@event_api.post("/add_related_event")
def add_related_event():
    pass

@event_api.post("/remove_related_event")
def remove_related_event():
    pass

@event_api.post("/add_param")
def add_event_param():
    pass

@event_api.post("/modify_param")
def modify_event_param():
    pass

@event_api.post("/remove_param")
def remove_event_param():
    pass

