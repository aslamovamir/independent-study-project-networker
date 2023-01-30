from backend.firebase.Firebase import database
from backend.model.user.User import User
from backend.model.user.UserModelHelper import UserModelHelper
from backend.helpers.MenuHelper import MenuHelper


class UserDBActions:
    
    # method to update the user node (modify or create a new) in the firebase
    def UpdateUser(user: User, collection: str = "Users") -> bool:
        try:
            database.child(collection).child(user.ID).set(UserModelHelper.UserToDictConvert(user=user))
            return True
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource="UserDBActions::UserDBActions:UpdateUser")