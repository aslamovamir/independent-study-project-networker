from firebase.Firebase import database
from model.user.User import User
from model.user.UserModelHelper import UserModelHelper
from helpers.MenuHelper import MenuHelper


class UserDBActions:
    
    # method to update the user node (modify or create a new) in the firebase
    def UpdateUser(user: User, collection: str = "Users") -> bool:
        try:
            database.child(collection).child(user.ID).set(UserModelHelper.UserToDictConvert(user=user))
            return True
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource="UserDBActions::UserDBActions:UpdateUser")