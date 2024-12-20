'''
Author: hushuhan 873933169@qq.com
Date: 2024-12-16 20:52:42
LastEditors: hushuhan 873933169@qq.com
LastEditTime: 2024-12-16 23:50:03
FilePath: \FavorSystem\entity.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel

class People(SQLModel, table=True):
    """
    Entity
    """
    id: Optional[int] = Field(default=None, primary_key=True, )
    name: str
    birthday: date = Field(default=None)
    gender: int
    favor: float = 0.0

class PeopleParam(SQLModel, tabel=True):
    """
    Relation
    """
    id: Optional[int] = Field(default=None, primary_key=True, )
    people_id: int
    param_key: str
    param_value: str

class Event(SQLModel, table=True):
    """
    Entity
    """
    id: Optional[int] = Field(default=None, primary_key=True, )
    owner_id: int # 事件拥有者
    event_date: date = Field(default=None) # 事件发生时间
    title: str
    description: str
    favor_effect: float

class EventRelatedPeople(SQLModel, table=True):
    """
    Relation
    """
    id: Optional[int] = Field(default=None, primary_key=True, )
    event_id: int
    related_id: int

class EventRelatedEvent(SQLModel, table=True):
    """
    Relation
    """
    id: Optional[int] = Field(default=None, primary_key=True, )
    event_id: int
    related_id: int

class EventParam(SQLModel, tabel=True):
    """
    Relation
    """
    id: Optional[int] = Field(default=None, primary_key=True, )
    event_id: int
    param_key: str
    param_value: str
