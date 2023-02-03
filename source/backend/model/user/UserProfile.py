from dataclasses import dataclass


@dataclass
class UserProfile:
    UserID: str
    Title: str
    About: str
    Gender: str
    Ethnicity: str
    DisabilityStatus: str
    Location: str
    PhoneNumber: str