from pydantic import BaseModel, computed_field
from datetime import datetime
from hashlib import sha256


class Event(BaseModel):
    name: str
    begin: datetime
    end: datetime
    description: str
    location: str
    url: str

    @computed_field
    @property
    def uid(self) -> str:
        return  sha256(f"{self.name}-{self.begin.isoformat()}-{self.end.isoformat()}".encode()).hexdigest()
