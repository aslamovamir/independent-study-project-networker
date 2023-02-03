from dataclasses import dataclass, field
from backend.model.user.Profile import Profile
from backend.helpers.MenuHelper import MenuHelper
from datetime import datetime

# A User entity.
@dataclass
class User:
    Id: str
    Username: str
    Email: str
    FirstName: str = ""
    LastName: str = ""
    Profile: Profile = None
    DateLastLogin: datetime = field(default_factory=datetime.now)
    DateRegistered: datetime = field(default_factory=datetime.now)

    # Hydrates a User entity using a pyrebase response value and returns it.
    def HydrateUser(user):
        return User(
                Id = UserHydrator.HydrateProp(user, "Id"),
                Username = UserHydrator.HydrateProp(user, "Username"),
                Email = UserHydrator.HydrateProp(user, "Email"),
                FirstName = UserHydrator.HydrateProp(user, "FirstName"),
                LastName = UserHydrator.HydrateProp(user, "LastName"),
                Profile = UserHydrator.HydrateProp(user, "Profile"),
                DateLastLogin = UserHydrator.HydrateProp(user, "DateLastLogin"),
                DateRegistered = UserHydrator.HydrateProp(user, "DateRegistered")
            )
    
    # method to convert User object to a dictionary
    def UserToDict(self) -> dict[str, str]:
        try:
            return {
                'Id': str(self.Id),
                'Username': str(self.Username),
                'Email': str(self.Email),
                'FirstName': str(self.FirstName),
                'LastName': str(self.LastName),
                'Profile': Profile.ProfileToDict(self.Profile),
                'DateLastLogin': str(self.DateLastLogin),
                'DateRegistered': str(self.DateRegistered)
            }
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource="UserModelHelper:UserToDictConvert")

class UserHydrator:
    
    # A dictionary to maintain the User entity's property name (key) and its type (value).
    _userAttributes: dict[str, str] = {
        "Id": "str",
        "Username": "str",
        "Email": "str",
        "FirstName": "str",
        "LastName": "str",
        "Profile": "Profile",
        "DateLastLogin": "datetime",
        "DateRegistered": "datetime"
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
        if propType == "Profile":
            profile: Profile = Profile.HydrateProfile(pyreValue)
            return profile
        
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
        elif propType == "Profile": return Profile()
        elif propType == "datetime": return datetime.min
        else: return None