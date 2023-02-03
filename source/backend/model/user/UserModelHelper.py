import hashlib
from backend.model.user.User import User
from backend.model.user.Profile import Profile
from backend.helpers.MenuHelper import MenuHelper


class UserModelHelper:

    # helper method to create a user id encrypted for the User class
    # we never statically store the password of the user for security purposes - instead, we hash password with username and pass it as ID
    def CreateUserID(username: str, password: str) -> str:
        return hashlib.sha256(str.encode(username.join(password))).hexdigest()

    
    # method to convert User object to a dictionary
    def UserToDictConvert(user: User) -> dict[str, str]:
        try:
            return {
                'ID': str(user.ID),
                'Username': str(user.Username),
                'Email': str(user.Email),
                'FirstName': str(user.FirstName),
                'LastName': str(user.LastName),
                'Profile': UserModelHelper.ProfileToDictConvert(user.Profile),
                'DateRegistered': str(user.DateRegistered),
                'DateLastLogin': str(user.DateLastLogin)
            }
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource="UserModelHelper:UserToDictConvert")


    # method to convert Profile object to a dictionary
    def ProfileToDictConvert(self):
        try:
            if self == None:
                self = Profile()
            
            if (self.EducationList == None):
                self.EducationList = []
            
            if (self.ExperienceList == None):
                self.ExperienceList = []

            return {
                'ID': str(self.Id),
                'Title': str(self.Title),
                'About': str(self.About),
                'Gender': str(self.Gender),
                'Ethnicity': str(self.Ethnicity),
                'DisabilityStatus': str(self.DisabilityStatus),
                'Location': str(self.Location),
                'PhoneNumber': str(self.PhoneNumber),
                'EducationList': {i: self.EducationList[i].EducationToDict() for i in range(len(self.EducationList))},
                'ExperienceList': {i: self.ExperienceList[i].ExpToDict() for i in range(len(self.ExperienceList))}
            }
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource="UserModelHelper:ProfileToDictConvert")