from helpers.MenuHelper import MenuHelper
from helpers.AuthenticationHelper import AuthenticationHelper
from model.user.User import User
from model.user.UserModelHelper import UserModelHelper
from database.UserDBActions import UserDBActions
from datetime import datetime


# method to add a new user
def RegisterNewUser() -> bool:
    MenuHelper.DefineSectionBreak()
    terminateOperation: bool = False

    # get a username
    while True:
        try:
            print("\nPlease enter a username")
            username: str = MenuHelper.InputStream()
            if username == "-1":
                terminateOperation = True
                break
            # check for empty input
            if MenuHelper.ValidateEmptyInput(input=username):
                MenuHelper.WarnInvalidInput()
                continue
            # TODO: check if the username entered is already in use in the database
            break
        except:
            MenuHelper.WarnInvalidInput()
    
    if terminateOperation:
        return True

    # get a password
    while True:
        try:
            print("\nNOTE: Password must be of size between 8 and 12, have at least one uppercase letter,",
            "one digit and one special character.")
            print("Please enter a password")
            password: str = MenuHelper.InputStream()
            if password == "-1":
                terminateOperation = True
                break
            # validate the password
            if not AuthenticationHelper.ValidatePassword(password=password):
                MenuHelper.WarnInvalidInput()
                continue
            break
        except:
            MenuHelper.WarnInvalidInput()

    if terminateOperation:
        return True
    
    # get an email address
    while True:
        try:
            print("\nPlease enter your email address")
            email: str = MenuHelper.InputStream()
            if email == "-1":
                terminateOperation = True
                break
            if not AuthenticationHelper.ValidateEmail(email=email):
                continue
            break
        except:
            MenuHelper.WarnInvalidInput()
        
    if terminateOperation:
        return True
    
    # get first name
    while True:
        try:
            print("\nPlease enter your first name")
            firstName: str = MenuHelper.InputStream()
            if firstName == "-1":
                terminateOperation = True
                break
            if MenuHelper.ValidateEmptyInput(input=firstName):
                MenuHelper.WarnInvalidInput()
                continue
            break
        except:
            MenuHelper.WarnInvalidInput()

    if terminateOperation:
        return True

    # get last name
    while True:
        try:
            print("\nPlease enter your last name")
            lastName: str = MenuHelper.InputStream()
            if lastName == "-1":
                terminateOperation = True
                break
            if MenuHelper.ValidateEmptyInput(input=lastName):
                MenuHelper.WarnInvalidInput()
                continue
            break
        except:
            MenuHelper.WarnInvalidInput()
    
    if terminateOperation:
        return True
    

    # now try to push the new user object to the database
    try:
        # user helper method to create hashed user ID
        userID: str = UserModelHelper.CreateUserID(username=username, password=password)
        operationResult: bool = UserDBActions.UpdateUser(user=User(
            ID=userID,
            Username=username,
            Email=email,
            FirstName=firstName,
            LastName=lastName,
            DateLastLogin=None,
            DateRegistered=datetime.now()
        ), collection="Users")

        if operationResult == False: raise Exception()

        return True

    except Exception as e:
        MenuHelper.DisplayErrorException(exception=e, errorSource="Signup::Signup::RegisterNewUser")
