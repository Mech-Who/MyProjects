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
    id: Optional[int] = Field(default=None, primary_key=True, )
    name: str
    birthday: date = Field(default=None)
    gender: int
    favor: float = 0.0
