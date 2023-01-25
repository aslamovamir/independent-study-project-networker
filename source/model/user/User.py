from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    ID: str
    Username: str
    Email: str
    FirstName: str
    LastName: str
    DateRegistered: datetime = field(default_factory=datetime.now)
    DateLastLogin: datetime = field(default_factory=datetime.now)