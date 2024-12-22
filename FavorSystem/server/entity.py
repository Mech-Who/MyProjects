from datetime import date

from sqlmodel import Field, SQLModel

class People(SQLModel, table=True):
    """
    Entity
    """
    id: int|None = Field(default=None, primary_key=True, )
    name: str|None = Field(index=True)
    birthday: date|None = Field(default=None, description="公历生日，精确到天")
    gender: int|None = Field(description="性别标识，0为女，1为男。")
    favor: float|None = Field(default=0.0, description="好感度值，最低为0，最高为100。")
    removed: int|None = Field(default=0, description="状态标记：0为正常，1为已删除，2为已存档。")

class PeopleParam(SQLModel, tabel=True):
    """
    Relation
    """
    id: int|None = Field(default=None, primary_key=True, )
    people_id: int|None = Field(foreign_key="people.id")
    param_key: str|None
    param_value: str|None
    removed: int|None = Field(default=0)

class Event(SQLModel, table=True):
    """
    Entity
    """
    id: int|None = Field(default=None, primary_key=True, )
    owner_id: int|None = Field(foreign_key="people.id") # 事件拥有者
    event_date: date|None = Field(default=None) # 事件发生时间
    title: str|None
    description: str|None
    favor_effect: float|None = Field(default=0.0)
    removed: int|None = Field(default=0)

class EventRelatedPeople(SQLModel, table=True):
    """
    Relation
    """
    id: int|None = Field(default=None, primary_key=True, )
    event_id: int|None = Field(foreign_key="event.id")
    related_id: int|None = Field(foreign_key="people.id")
    removed: int|None = Field(default=0)

class EventRelatedEvent(SQLModel, table=True):
    """
    Relation
    """
    id: int|None = Field(default=None, primary_key=True, )
    event_id: int|None = Field(foreign_key="event.id")
    related_id: int|None = Field(foreign_key="event.id")
    removed: int|None = Field(default=0)

class EventParam(SQLModel, tabel=True):
    """
    Relation
    """
    id: int|None = Field(default=None, primary_key=True, )
    event_id: int|None = Field(foreign_key="event.id")
    param_key: str|None
    param_value: str|None
    removed: int|None = Field(default=0)
