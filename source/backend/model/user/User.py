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

    # Hydrates a User entity using a pyrebase response value and returns it.
    def HydrateUser(user):
        return User(
                ID = UserHydrator.HydrateProp(user, "ID"),
                Username = UserHydrator.HydrateProp(user, "Username"),
                Email = UserHydrator.HydrateProp(user, "Email"),
                FirstName = UserHydrator.HydrateProp(user, "FirstName"),
                LastName = UserHydrator.HydrateProp(user, "LastName"),
                DateRegistered = UserHydrator.HydrateProp(user, "DateRegistered"),
                DateLastLogin = UserHydrator.HydrateProp(user, "DateLastLogin")
            )


class UserHydrator:
    
    # A dictionary to maintain the User entity's property name (key) and its type (value).
    _userAttributes: dict[str, str] = {
        "ID": "str",
        "Username": "str",
        "Email": "str",
        "FirstName": "str",
        "LastName": "str",
        "DateRegistered": "datetime",
        "DateLastLogin": "datetime"
    }
    
    # Hydrates an individual property for the User entity.
    def HydrateProp(user, prop: str):
        if prop not in UserHydrator._userAttributes.keys():
            raise Exception(f"Property {prop} not defined for entity: User")
        
        propType: str = UserHydrator._userAttributes.get(prop)
        value = None
        
        try:
            pyreValue = user.val()[prop]
            value = UserHydrator.Cast(pyreValue, propType)
        except:
            value = UserHydrator.GetDefaultValue(prop)
        
        if value == None: raise Exception(f"Could not hydrate prop: {prop} for User")
        
        return value
    
    # Handles conversion to a certain type.
    def Cast(pyreValue, propType):
        if propType == "datetime":
            datetimeValue: datetime = datetime.fromisoformat(pyreValue)
            return datetimeValue
        
        return pyreValue
        
    # Gets the default value for a property on the User entity based on its type.
    def GetDefaultValue(prop: str):
        propType: str = UserHydrator._userAttributes.get(prop)

        if propType == "str": return ""
        elif propType == "bool": return True
        elif propType == "dict[str, bool]": return {}
        elif propType == "datetime": return datetime.min
        else: return None