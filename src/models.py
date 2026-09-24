from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
    name: str
    begin: datetime
    end: datetime
    description: str
    location: str
    url: str
