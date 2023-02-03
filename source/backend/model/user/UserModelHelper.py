import hashlib
from backend.model.user.User import User
from backend.model.user.UserProfile import UserProfile


class UserModelHelper:

    # helper method to create a user id encrypted for the User class
    # we never statically store the password of the user for security purposes - instead, we hash password with username and pass it as ID
    def CreateUserID(username: str, password: str) -> str:
        return hashlib.sha256(str.encode(username.join(password))).hexdigest()

    
    # method to convert User object to a dictionary
    def UserToDictConvert(user: User) -> dict[str, str]:
        return {
            'ID': str(user.ID),
            'Username': str(user.Username),
            'Email': str(user.Email),
            'FirstName': str(user.FirstName),
            'LastName': str(user.LastName),
            'DateRegistered': str(user.DateRegistered),
            'DateLastLogin': str(user.DateLastLogin)
        }


    # method to convert UserProfile object to a dictionary
    def UserProfileToDictConvert(userProfile: UserProfile) -> dict[str, str]:
        return {
            'UserID': str(userProfile.UserID),
            'Title': str(userProfile.Title),
            'About': str(userProfile.About),
            'Gender': str(userProfile.Gender),
            'Ethnicity': str(userProfile.Ethnicity),
            'DisabilityStatus': str(userProfile.DisabilityStatus),
            'Location': str(userProfile.Location),
            'PhoneNumber': str(userProfile.PhoneNumber)
        }