from typing import List, Literal
from pydantic import BaseModel, Field


class Entity(BaseModel):
   text:str = Field()
   type: Literal["SKILL","JOB_TITLE"]


class Labels(BaseModel):
   Entities: List[Entity]