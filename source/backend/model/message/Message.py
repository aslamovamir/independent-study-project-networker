from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Message:
    Id: str
    SenderId: str
    SenderUsername: str
    ReceiverId: str
    Content: str
    IsRead: bool = False
    DateCreated: datetime = field(default_factory=datetime.now)

     # Hydrates a Message entity using a pyrebase response value and returns it.
    def HydrateMessage(message):
        return Message(
            Id = MessageHydrator.HydrateProp(message, "Id"),
            SenderId = MessageHydrator.HydrateProp(message, "SenderId"),
            SenderUsername = MessageHydrator.HydrateProp(message, "SenderUsername"),
            ReceiverId = MessageHydrator.HydrateProp(message, "ReceiverId"),
            Content = MessageHydrator.HydrateProp(message, "Content"),
            IsRead = MessageHydrator.HydrateProp(message, "IsRead"),
            DateCreated = MessageHydrator.HydrateProp(message, "DateCreated")
        )
    
    # Converts a message entity into a dictionary.
    def MessageToDict(self) -> dict:
        return {
            'Id': str(self.Id),
            'SenderId': str(self.SenderId),
            'SenderUsername': str(self.SenderUsername),
            'ReceiverId': str(self.ReceiverId),
            'Content': str(self.Content),
            'IsRead': str(self.IsRead),
            'DateCreated': str(self.DateCreated)
        }
    

class MessageHydrator:

    # A dictionary to maintain the Message entity's property name (key) and its type (value).
    _messageAttributes: dict[str, str] = {
        "Id": "int",
        "SenderId": "str",
        "SenderUsername": "str",
        "ReceiverId": "str",
        "Content": "str",
        "IsRead": "bool",
        "DateCreated": "datetime"
    }


    # Hydrates an individual property for the Message entity.
    def HydrateProp(message, prop: str):
        if prop not in MessageHydrator._messageAttributes.keys():
            raise Exception(f"Property {prop} not defined for entity: Message")
        
        propType: str = MessageHydrator._messageAttributes.get(prop)
        value = None
        
        try:
            value = MessageHydrator.Cast(message.val()[prop], propType)
        except:
            value = MessageHydrator.GetDefaultValue(prop)
        
        if value == None: raise Exception(f"Could not hydrate prop: {prop} for Message")
        
        return value


    # Handles conversion to a certain type.
    def Cast(pyreValue, propType):
        if propType == "bool":
            return eval(pyreValue)
        
        if propType == "int":
            return int(pyreValue)
        
        if propType == "datetime":
            datetimeValue: datetime = datetime.fromisoformat(pyreValue)
            return datetimeValue
        
        return pyreValue

    # Gets the default value for a property on the Message entity based on its type.
    def GetDefaultValue(prop: str):
        propType: str = MessageHydrator._messageAttributes.get(prop)

        if propType == "int": return 0
        if propType == "str": return ""
        elif propType == "bool": return False
        elif propType == "datetime": return datetime.min
        else: return None