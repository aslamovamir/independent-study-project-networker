from flask import Flask, render_template, session, request, redirect, flash, url_for
from backend.helpers.AuthenticationHelper import AuthenticationHelper
from backend.model.user.User import User
from backend.model.user.UserModelHelper import UserModelHelper
from backend.database.UserDBActions import UserDBActions
from backend.helpers.MenuHelper import MenuHelper
from datetime import datetime

app = Flask(__name__)
app.secret_key="networker-app-20190805"
LoggedUser: User = None

# Routes build-up
@app.route('/', methods=['POST', 'GET'])
def index():
    error = None
    if request.method == "POST":
        # get the entries from the user
        username: str = request.form.get('username')
        password: str = request.form.get('password')

        try: 
            # create the encrypted user ID for the entered username and password
            userId: str = UserModelHelper.CreateUserID(username=username, password=password)

            # get all users
            allUsers = UserDBActions.GetAllUsers()

            if (allUsers == None):
                raise Exception()

            global LoggedUser
            userFound: bool = False
            # now check the ID of all users
            for user in allUsers:
                if user.Id == userId:
                    userFound = True
                    # log the user
                    LoggedUser = user
                    break
            if userFound:
                # now update the user with the new logged in date in the database
                LoggedUser.DateLastLogin = datetime.now()
                UserDBActions.UpdateUser(user=LoggedUser)

                return render_template('dashboard.html', loggedUser=LoggedUser)
            else:
                error = "User Not Found"

        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource="app::index")

    return render_template('index.html', error=error)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    error = None
    if request.method == "POST":
        # get the entries the user
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        email: str = request.form.get('email')
        firstName: str = request.form.get('first-name')
        lastName: str = request.form.get('last-name')

        # now check if the entered username does not already exist in the database
        username_exists: bool = False
        users: list[User] = UserDBActions.GetAllUsers()
        if (users != None):
            for user in users:
                if user.Username == username:
                    username_exists = True

        if not username_exists:
            # now validate password
            if AuthenticationHelper.ValidatePassword(password=password):
                # now try to push the new user object to the database
                try:
                    # user helper method to create hashed user ID
                    userId: str = UserModelHelper.CreateUserID(username=username, password=password)
                    operationResult: bool = UserDBActions.UpdateUser(user=User(
                        Id=userId,
                        Username=username,
                        Email=email,
                        FirstName=firstName,
                        LastName=lastName,
                        DateLastLogin=None,
                        DateRegistered=datetime.now()
                    ), collection="Users")

                    if operationResult == False: raise Exception()
                    else: flash("Success: You have successfully signed up.")
                except Exception as e:
                    MenuHelper.DisplayErrorException(exception=e, errorSource="Signup::Signup::RegisterNewUser")
            else:
                error = "Invalid password."
        else:
            error = "This username already exists."

    return render_template('signup.html', error=error)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/update_profile')
def update_profile():
    return render_template('update_profile.html', loggedUser=LoggedUser)








@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/terms_of_use')
def terms_of_use():
    return render_template('terms_of_use.html')



# run of the app
if __name__ == '__main__':
    app.run(debug = True)