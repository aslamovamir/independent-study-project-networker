import hashlib
from backend.model.user.User import User


class UserModelHelper:

    # helper method to create a user id encrypted for the User class
    # we never statically store the password of the user for security purposes - instead, we hash password with username and pass it as ID
    def CreateUserID(username: str, password: str) -> str:
        return hashlib.sha256(str.encode(username.join(password))).hexdigest()

    
    # method to convert User object to a dictionary
    def UserToDictConvert(user: User) -> dict:
        return {
            'ID': str(user.ID),
            'Username': str(user.Username),
            'Email': str(user.Email),
            'FirstName': str(user.FirstName),
            'LastName': str(user.LastName),
            'DateRegistered': str(user.DateRegistered),
            'DateLastLogin': str(user.DateLastLogin)
        }