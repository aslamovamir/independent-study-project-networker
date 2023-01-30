from flask import Flask, render_template, session, request, redirect, flash
from backend.helpers.AuthenticationHelper import AuthenticationHelper
from backend.model.user.User import User
from backend.model.user.UserModelHelper import UserModelHelper
from backend.database.UserDBActions import UserDBActions
from datetime import datetime

app = Flask(__name__)


# Routes build-up
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    message = None
    if request.method == "POST":
        # get the entries entered by the user
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        email: str = request.form.get('email')
        firstName: str = request.form.get('first-name')
        lastName: str = request.form.get('last-name')

        # first validate password
        if AuthenticationHelper.ValidatePassword(password=password):
            flash("Trying to register a new account for you!")
        else:
            message = "Invalid Password"


        

    return render_template('signup.html')







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