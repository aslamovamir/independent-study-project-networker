from flask import Flask, render_template, session, request, redirect, flash, url_for
from backend.helpers.AuthenticationHelper import AuthenticationHelper
from backend.model.user.User import User
from backend.model.user.Profile import Profile
from backend.model.job.Job import Job
from backend.model.job.AppliedJob import AppliedJob
from backend.model.message.Message import Message
from backend.model.post.Post import Post
from backend.model.job.JobModelHelper import JobModelHelper
from backend.model.user.UserModelHelper import UserModelHelper
from backend.model.post.PostModelHelper import PostModelHelper
from backend.database.UserDBActions import UserDBActions
from backend.database.JobDBActions import JobDBActions
from backend.database.FriendsDBActions import FriendsDBActions
from backend.database.MessageDBActions import MessageDBActions
from backend.database.PostDBActions import PostDBActions
from backend.helpers.MenuHelper import MenuHelper
from datetime import datetime
import smtplib
from email.message import EmailMessage

# SECRETS (MUST BE STORED SOMEWHERE ELSE OR AT ENVIRONMENT LEVEL)
_APP_SECRET_KEY = "networker-app-20190805"
_EMAIL_SERVER_SECRET_USERNAME = "networkeremailserver@gmail.com"
_EMAIL_SERVER_SECRET_APP_PASSWORD = "ikbfdabbziutojmg"
_EMAIL_SERVER_SECRET_PLATFORM = "smtp.gmail.com"
_EMAIL_SERVER_SECRET_PLATFORM_NUMBER = 587


app = Flask(__name__)
app.secret_key=_APP_SECRET_KEY

email_server = smtplib.SMTP(_EMAIL_SERVER_SECRET_PLATFORM, _EMAIL_SERVER_SECRET_PLATFORM_NUMBER)
email_server.starttls()
email_server.login(_EMAIL_SERVER_SECRET_USERNAME, _EMAIL_SERVER_SECRET_APP_PASSWORD)

LoggedUser: User = None

# Routes build-up
@app.route('/', methods=['POST', 'GET'])
def index():
    error = None
    success = None

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
                success = "Successfully logged in"
                # now update the user with the new logged in date in the database
                LoggedUser.DateLastLogin = datetime.now()
                UserDBActions.UpdateUser(user=LoggedUser)

                # get all new posts
                posts: list[Post] = []
                try:
                    posts = PostDBActions.GetAllPosts()
                    if posts == None:
                        posts = []
                except Exception as e:
                    MenuHelper.DisplayErrorException(exception=e, errorSource='/GetAllPosts')

                return render_template('dashboard.html', loggedUser=LoggedUser, posts=posts, success=success)
            else:
                error = "User not found!"

        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource="/")

    return render_template('index.html', error=error)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    error = None
    success = None

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
                    ))

                    if operationResult == False:
                        error = "Could not create a new account, somethong went wrong!" 
                        raise Exception()
                    else:
                        success = "Successfully registered a new account"
                        # now send an automated email to the new user with welcome message
                        message = EmailMessage()
                        message['Subject'] = "Signup Successful at Networker!"
                        message['From'] = "networkeremailserver@gmail.com"
                        message['To'] = email
                        message.set_content("Thanks for signing up for Networker!")
                        # email_server.send_message(message)

                except Exception as e:
                    MenuHelper.DisplayErrorException(exception=e, errorSource="signup/UpdateUser")
            else:
                error = "Invalid password!"
        else:
            error = "This username already exists!"

    return render_template('signup.html', error=error, success=success)


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    global LoggedUser
    error = None
    success = None
    showComment: bool = False
    commentToShow: str = None

    if request.method == 'POST':
        likeBtnClicked = request.form.get('likeBtn')
        if likeBtnClicked != None:
            postId: str = likeBtnClicked
            # get the post object from the database
            try:
                post: Post = PostDBActions.GetPostById(postId=postId)
                if post == None: raise Exception("Error! The post does not exist in the database.")
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='dashboard/PostDBActions/GetPostById')
            # now evaluate the post positively
            try:
                operationResult: bool = PostDBActions.Evaluate(userId=LoggedUser.Id, post=post, like=True)
                if operationResult == False:
                    error = "Could not complete the like operation, something went wrong!"
                    raise Exception()
                else:
                    success = "The post liked"
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='dashboard/PostDBActions/Evaluate')

        dislikeBtnClicked = request.form.get('dislikeBtn')
        if dislikeBtnClicked != None:
            postId: str = dislikeBtnClicked
            # get the post object from the database
            try:
                post: Post = PostDBActions.GetPostById(postId=postId)
                if post == None: raise Exception("Error! The post does not exist in the database.")
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='dashboard/PostDBActions/GetPostById')
            # now evaluate the post negatively
            try:
                operationResult: bool = PostDBActions.Evaluate(userId=LoggedUser.Id, post=post, like=False)
                if operationResult == False:
                    error = "Could not complete the dislike operation, something went wrong!"
                    raise Exception()
                else:
                    success = "The post disliked"
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='dashboard/PostDBActions/Evaluate')

        commentBtnClicked = request.form.get('commentBtn')
        if commentBtnClicked != None:
            commentToShow = commentBtnClicked
            showComment = True

        addCommentBtnClicked = request.form.get('addCommentBtn')
        if addCommentBtnClicked != None:
            postId: str = addCommentBtnClicked
            # get the post object from the database
            try:
                post: Post = PostDBActions.GetPostById(postId=postId)
                if post == None: raise Exception("Error! The post does not exist in the database.")
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='dashboard/PostDBActions/GetPostById')
            # get the content of the comment
            comment: str = request.form.get('comment')
            # now add the comment to the post
            try:
                operationResult: bool = PostDBActions.Comment(user=LoggedUser.Username + " | " + LoggedUser.FirstName+" "+LoggedUser.LastName, post=post, comment=comment)
                if operationResult == False:
                    error = "Could not complete the comment operation, something went wrong!"
                    raise Exception()
                else:
                    success = "The post commented"
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='dashboard/Comment')

    # get all new posts
    posts: list[Post] = []
    try:
        posts = PostDBActions.GetAllPosts()
        if posts == None:
            posts = []
    except Exception as e:
        MenuHelper.DisplayErrorException(exception=e, errorSource='dashboard/GetAllPosts')

    return render_template('dashboard.html', loggedUser=LoggedUser, posts=posts, showComment=showComment, commentToShow=commentToShow, error=error, success=success)


@app.route('/update_profile', methods=['POST', 'GET'])
def update_profile():
    error = None
    success = None

    if request.method == "POST":
        global LoggedUser
        # get the entries form the form and update the profile
        form_entree: str = request.form.get('first-name')
        if form_entree != "":
            LoggedUser.FirstName = form_entree

        form_entree = request.form.get('last-name')
        if form_entree != "":
            LoggedUser.LastName = form_entree

        form_entree = request.form.get('email')
        if form_entree != "":
            LoggedUser.Email = form_entree    
        
        # to update profile, first need to check if the user already had a profile
        profile: Profile = None
        if LoggedUser.Profile != None and LoggedUser.Profile != Profile():
            profile = LoggedUser.Profile
        else:
            profile = Profile()
        
        # now update the attributes of the profile
        form_entree = request.form.get('title')
        if form_entree != "":
            profile.Title = form_entree
        
        form_entree = request.form.get('about')
        if form_entree != "":
            profile.About = form_entree

        form_entree = request.form.get('gender')
        if form_entree != "":
            profile.Gender = form_entree

        form_entree = request.form.get('ethnicity')
        if form_entree != "":
            profile.Ethnicity = form_entree

        form_entree = request.form.get('disability-status')
        if form_entree != "":
            profile.DisabilityStatus = form_entree

        form_entree = request.form.get('location')
        if form_entree != "":
            profile.Location = form_entree

        form_entree = request.form.get('phone-number')
        if form_entree != "":
            profile.PhoneNumber = form_entree    

        # now assign the profile variable to the logged user's profile
        LoggedUser.Profile = profile
        # now update the user in the database
        try:
            operationResult: bool = UserDBActions.UpdateUser(user=LoggedUser)
            if operationResult == False:
                error = "Could not update the account, something went wrong!"
                raise Exception()
            else:
                success = "Account successfully updated"
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource="update_profile/UpdateUser")

    return render_template('update_profile.html', loggedUser=LoggedUser, error=error, success=success)


@app.route('/create_job_posting', methods=['POST', 'GET'])
def create_job_posting():
    global LoggedUser
    error = None
    success = None

    if request.method == 'POST':
        # get the entries from the form
        title: str = request.form.get('title')
        employer: str = request.form.get('employer')
        industry: str = request.form.get('industry')
        location: str = request.form.get('location')
        salary: str = request.form.get('salary')
        description: str = request.form.get('description')

        # now try to create a new job object and push it to the database
        try:
            jobId: str = JobModelHelper.CreateJobID(
                title=title,
                employer=employer,
                industry=industry,
                description=description,
                location=location,
                salary=salary
            )

            operationResult: bool = JobDBActions.UpdateJob(job=Job(
                Id=jobId,
                Title=title,
                Employer=employer,
                Industry=industry,
                Description=description,
                Location=location,
                Salary=salary,
                PosterId=LoggedUser.Id,
                DateCreated=datetime.now()
            ))

            if operationResult == False:
                error = "Could not create job posting, something went wrong!"
                raise Exception()
            else:
                success = "Job posting successfully created"
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource="create_job_posting/CreateJobID")

    return render_template('create_job_posting.html', loggedUser=LoggedUser, error=error, success=success)


@app.route('/apply_for_job', methods=['POST', 'GET'])
def apply_for_job():
    global LoggedUser
    error = None

    # get all the jobs created by others
    jobs: list[Job] = []
    try:
        jobs = JobDBActions.GetAllJobsOffUser(userId=LoggedUser.Id)
        if jobs == None:
            jobs = []
    except Exception as e:
        MenuHelper.DisplayErrorException(exception=e, errorSource="apply_for_job/GetAllJobsOffUser")

    if request.method == 'POST':
        # get the id of the job clicked by the user via the button assigned to it
        jobIdToApply: str = request.form['applyBtn']
        # now check if the user already applied for this job
        try:
            if JobDBActions.CheckIfApplied(userId=LoggedUser.Id, jobId=jobIdToApply):
                error = "You have already applied for this job!"
                return render_template('apply_for_job.html', jobs=jobs, error=error)
        except Exception as e:
            MenuHelper.DisplayErrorException(errorSource='apply_for_job/CheckIfApplied')
        # get the job
        for job in jobs:
            if job.Id == jobIdToApply:
                jobToApply: Job = job
        # now redirect to a new application page, with the job id and the logged user
        return render_template('application.html', job=jobToApply)

    return render_template('apply_for_job.html', jobs=jobs, error=error)


@app.route('/application', methods=['POST', 'GET'])
def application():
    global LoggedUser
    error = None
    success = None

    jobToApply = None

    if request.method == 'POST':
        # get the id of the job picked via the apply button
        jobId: str = request.form['applyBtn']
        # now get all the form fields
        startDate: datetime = request.form.get('start_date')
        sponsorshipRequirement: str = request.form.get('sponsorship_requirement')
        goodFitReasoning: str = request.form.get('good_fit_reasoning')
        # assign the custom values
        userId: str = LoggedUser.Id
        id: str = JobModelHelper.CreateAppliedJobID(userId=userId, jobId=jobId)
        userName: str = LoggedUser.LastName + ", " + LoggedUser.FirstName
        dateApplied: datetime = datetime.now()
        status: str = 'Unreviewed'
        # get the job from its id
        job: Job = JobDBActions.GetJobFromId(jobId=jobId)
        jobToApply = job
        jobTitle: str = job.Title
        jobEmployer: str = job.Employer
        posterId: str = job.PosterId

        # now try to push the applied job to the database
        try:
            operationResult: bool = JobDBActions.UpdateAppliedJob(AppliedJob(
                Id=id,
                UserId=userId,
                PosterId=posterId,
                UserName=userName,
                JobId=jobId,
                JobTitle=jobTitle,
                JobEmployer=jobEmployer,
                Status=status,
                StartDate=startDate,
                GoodFitReasoning=goodFitReasoning,
                SponsorshipRequirement=sponsorshipRequirement,
                DateApplied=dateApplied,
                DateReviewed=None
            ))

            if operationResult == False:
                error = "Could not complete application for the job posting, something went wrong!"
                raise Exception()
            else:
                success = "Application for the job successfully completed"
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource='application/JobDBActions/UpdateAppliedJob')

    return render_template('application.html', job=jobToApply, error=error, success=success)


@app.route('/applied_jobs')
def applied_jobs():
    global LoggedUser
    # get all the applied jobs of the logged user
    appliedJobs: list[AppliedJob] = []
    try:
        appliedJobs = JobDBActions.GetAllAppliedJobsUser(userId=LoggedUser.Id)
        if appliedJobs == None:
            appliedJobs = []
    except Exception as e:
        MenuHelper.DisplayErrorException(exception=e, errorSource='applied_jobs/GetAllAppliedJobsUser')

    return render_template('applied_jobs.html', jobs=appliedJobs)


@app.route('/review_applications', methods=['POST', 'GET'])
def review_applications():
    global LoggedUser
    error = None
    success = None

    if request.method == 'POST':
        applyBtnClicked = request.form.get('acceptBtn')
        if applyBtnClicked != None:
            appliedJobId: str = applyBtnClicked
            # change the status and the date of the applied job
            try:
                job: AppliedJob = JobDBActions.GetAppliedJobFromId(jobId=appliedJobId)
                # now upate the status and the review date of the job
                job.Status = "Approved"
                job.DateReviewed = datetime.now()
                operationResult: bool = JobDBActions.UpdateAppliedJob(appliedJob=job)
                if operationResult == False:
                    error = "Could change the status of the application to approved, something went wrong!"
                    raise Exception()
                else:
                    success = "Successfully changed the status of the application to approved"
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='review_applications/GetAppliedJobFromId')

        rejectBtnClicked = request.form.get('rejectBtn')
        if rejectBtnClicked != None:
            appliedJobId: str = rejectBtnClicked
            # change the status and the date of the applied job
            try:
                job: AppliedJob = JobDBActions.GetAppliedJobFromId(jobId=appliedJobId)
                # now upate the status and the review date of the job
                job.Status = "Rejected"
                job.DateReviewed = datetime.now()
                operationResult: bool = JobDBActions.UpdateAppliedJob(appliedJob=job)
                if operationResult == False:
                    error = "Could change the status of the application to approved, something went wrong!"
                    raise Exception()
                else:
                    success = "Successfully changed the status of the application to rejected"
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='review_applications/GetAppliedJobFromId')

    # get all the applied jobs posted by the logged user
    jobsPosted: list[AppliedJob] = []
    try:
        jobsPosted = JobDBActions.GetAllAppliedJobsPosterUser(userId=LoggedUser.Id)
        if jobsPosted == None:
            jobsPosted = []
    except Exception as e:
        MenuHelper.DisplayErrorException(exception=e, errorSource='review_applications/GetAllAppliedJobsPosterUser')

    return render_template('review_applications.html', jobs=jobsPosted, error=error, success=success)


@app.route('/my_network', methods=['POST', 'GET'])
def my_network():
    global LoggedUser
    error = None
    success = None

    if request.method == 'POST':
        # get the id of the user selected to connect to
        userId: str = request.form['connBtn']
        # now get the user object out of the user id
        try:
            user = UserDBActions.GetUserById(userId=userId)
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource='my_network/GetUserById')
        # now check if the logged user has already sent a friend request to this user
        if LoggedUser.Username in user.Friends:
            error = "You have already sent a friend request to this user!"
        else:
            # now try to push the new user in the list of connections of the logged user
            try:
                operationResult: bool = FriendsDBActions.SendFriendRequest(sender=LoggedUser, receiver=user)
                if operationResult == False:
                    error = "Could not send friend request to the user, something went wrong!"
                    raise Exception()
                else:
                    success = "Friend request successfully sent to the user"
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='my_network/SendFriendRequest')

    # get all the users except for the logged user
    users: list[User] = []
    try:
        users = UserDBActions.GetAllUsersOffUser(userId=LoggedUser.Id)
        if users == None:
            users = []
    except Exception as e:
        MenuHelper.DisplayErrorException(exception=e, errorSource='my_network/GetAllUsersOffUser')

    return render_template('my_network.html', users=users, error=error, success=success)


@app.route('/pending_requests', methods=['POST', 'GET'])
def pending_requests():
    global LoggedUser
    error = None
    success = None

    if request.method == 'POST':
        acceptBtnClicked = request.form.get('acceptBtn')
        if acceptBtnClicked != None:
            # get the id of the user selected to connect to
            userId: str = acceptBtnClicked
            # now get the user object out of the user id
            try:
                user = UserDBActions.GetUserById(userId=userId)
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='pending_requests/GetUserById')
            # now confirm the friends connection on both receiver and sender
            try:
                operationResult: bool = FriendsDBActions.AcceptFriendRequest(user=LoggedUser, userToAdd=user)
                if operationResult == False:
                    error = "Could not accept friend request from the user, something went wrong!"
                    raise Exception()
                else:
                    success = "Successfully accepted friend request from the user, this user is added to your connections"
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='pending_requests/AcceptFriendRequest')
        
        rejectBtnClicked = request.form.get('rejectBtn')
        if rejectBtnClicked != None:
            userId: str = rejectBtnClicked
            # now get the user object out of the user id
            try:
                user = UserDBActions.GetUserById(userId=userId)
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='pending_requests/GetUserById')
            # now reject the friend request
            try:
                operationResult: bool = FriendsDBActions.RejectFriendRequest(user=LoggedUser, userToReject=user)
                if operationResult == False:
                    error = "Could not reject friend request from the user, something went wrong!"
                    raise Exception()
                else:
                    success = "Successfully rejected friend request from the user"
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='pending_requests/RejectFriendRequest')
        
    # get all the pending friends of the logged user
    users: list[User] = []
    try:
        users = FriendsDBActions.GetPendingRequests(userName=LoggedUser.Username)
        if users == None:
            users = []
    except Exception as e:
        MenuHelper.DisplayErrorException(exception=e, errorSource='pending_requests/GetPendingRequests')
    
    return render_template('pending_requests.html', users=users, error=error, success=success)


@app.route('/my_connections', methods=['POST', 'GET'])
def my_connections():
    global LoggedUser
    error = None
    success = None

    if request.method == 'POST':
        messageBtnClicked = request.form.get('messageBtn')
        if messageBtnClicked != None:
            userId: str = messageBtnClicked
            # now get the user object out of the user id
            try:
                user = UserDBActions.GetUserById(userId=userId)
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='my_connections/GetUserById')
            # now call the function of the page that gets message content
            return render_template('message.html', receiver=user)

        disconnectBtnClicked = request.form.get('disConnBtn')
        if disconnectBtnClicked != None:
            # get the id of the user selected to connect to
            userId: str = disconnectBtnClicked
            # now get the user object out of the user id
            try:
                user = UserDBActions.GetUserById(userId=userId)
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='my_connections/GetUserById')
            # now remove the friend
            try:
                operationResult: bool = FriendsDBActions.DeleteFriend(user=LoggedUser, userToDelete=user)
                if operationResult == False:
                    error = "Could not disconnect the user, something went wrong!"
                    raise Exception()
                else:
                    success = "The user disconnected successfully, the user removed from your connections"
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='my_connections/DeleteFriend')

    # get the list of all connected friends of the logged user
    users: list[User] = []
    try:
        users = FriendsDBActions.GetFriends(username=LoggedUser.Username)
        if users == None:
            users = []
    except Exception as e:
        MenuHelper.DisplayErrorException(exception=e, errorSource='my_connections/GetFriends')

    return render_template('my_connections.html', users=users, error=error, success=success)


@app.route('/my_inbox', methods=['POST', 'GET'])
def my_inbox():
    global LoggedUser
    error = None
    success = None

    # get all received messages of the user
    messages: list[Message] = []
    try:
        messages = MessageDBActions.GetAllReceivedMessages(userId=LoggedUser.Id)
        if messages == None:
            messages = []
    except Exception as e:
        MenuHelper.DisplayErrorException(exception=e, errorSource='my_inbox/GetReceivedMessages')
    messages.sort(key=lambda x: x.DateCreated, reverse=True)

    if request.method == 'POST':
        viewBtnClicked = request.form.get('viewBtn')
        if viewBtnClicked != None:
            senderId: str = viewBtnClicked
            # now get all the messages received from the user to the logged user
            messagesReceived: list[Message] = []
            try:
                messagesReceived = MessageDBActions.GetAllReceivedMessagesFromUser(receiverId=LoggedUser.Id, senderId=senderId)
                if messagesReceived == None:
                    messagesReceived = []
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='my_inbox/GetAllReceivedMessagesFromUser')

            # now get all the messages sent to the user from the logged user
            messagesSent: list[Message] = []
            try:
                messagesSent = MessageDBActions.GetAllReceivedMessagesFromUser(receiverId=senderId, senderId=LoggedUser.Id)
                if messagesSent == None:
                    messagesSent = []
            except Exception as e:
                MenuHelper.DisplayErrorException(exception=e, errorSource='my_inbox/GetAllReceivedMessagesFromUser')

            # now create a list object to contain message contents only
            contents = []
            for message in messagesReceived:
                contents.append({
                    "received": True,
                    "content": message.Content,
                    "date": message.DateCreated
                })
            for message in messagesSent:
                contents.append({
                    "received": False,
                    "content": message.Content,
                    "date": message.DateCreated
                })
            # now sort the list by date
            contents.sort(key=lambda x: x['date'], reverse=False)
            # get the id of the user to respond to
            respondentId: str = senderId
            
            return render_template('my_inbox.html', messages=messages, contents=contents, respondentId=respondentId)
        
        replyBtnClicked = request.form.get('replyBtn')
        if replyBtnClicked != None:
            if replyBtnClicked == "None":
                error = "No respondent to reply to!"
            else:    
                respondentId: str = replyBtnClicked
                response: str = request.form.get('response')
                # now send the message to the respondent from the logged user
                try:
                    operationResult: bool = MessageDBActions.SendMessage(
                        senderId=LoggedUser.Id, sender=LoggedUser.FirstName + " " + LoggedUser.LastName + " | " + 
                        LoggedUser.Username, receiverId=respondentId, content=response)
                    if operationResult == False:
                        error = "Could not send the message to the user, something went wrong!"
                        raise Exception()
                    else:
                        success = "Message sent to the user successfully"
                except Exception as e:
                    MenuHelper.DisplayErrorException(exception=e, errorSource='my_inbox/SendMessage')
            
                messagesReceived: list[Message] = []
                try:
                    messagesReceived = MessageDBActions.GetAllReceivedMessagesFromUser(receiverId=LoggedUser.Id, senderId=respondentId)
                    if messagesReceived == None:
                        messagesReceived = []
                except Exception as e:
                    MenuHelper.DisplayErrorException(exception=e, errorSource='my_inbox/GetAllReceivedMessagesFromUser')

                # now get all the messages sent to the user from the logged user
                messagesSent: list[Message] = []
                try:
                    messagesSent = MessageDBActions.GetAllReceivedMessagesFromUser(receiverId=respondentId, senderId=LoggedUser.Id)
                    if messagesSent == None:
                        messagesSent = []
                except Exception as e:
                    MenuHelper.DisplayErrorException(exception=e, errorSource='my_inbox/GetAllReceivedMessagesFromUser')

                # now create a list object to contain message contents only
                contents = []
                for message in messagesReceived:
                    contents.append({
                        "received": True,
                        "content": message.Content,
                        "date": message.DateCreated
                    })
                for message in messagesSent:
                    contents.append({
                        "received": False,
                        "content": message.Content,
                        "date": message.DateCreated
                    })
                # now sort the list by date
                contents.sort(key=lambda x: x['date'], reverse=False)

                return render_template('my_inbox.html', messages=messages, contents=contents, respondentId=respondentId, error=error, success=success)


    return render_template('my_inbox.html', messages=messages, respondentId=None, error=error, success=success)


@app.route('/message', methods=['POST', 'GET'])
def message():
    global LoggedUser
    receiver = None
    error = None
    success = None

    if request.method == 'POST':
        # get the message content from the form
        content: str = request.form.get('content')
        # get the id of the receiver
        receiverId: str = request.form['sendBtn']
        # now get the user object out of the user id
        try:
            receiver = UserDBActions.GetUserById(userId=receiverId)
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource='message/GetUserById')
        # now send the message
        try:
            operationResult: bool = MessageDBActions.SendMessage(
                senderId=LoggedUser.Id, sender=LoggedUser.FirstName + " " + LoggedUser.LastName + " | " + 
                LoggedUser.Username, receiverId=receiverId, content=content)
            if operationResult == False:
                error = "Could not send the message to the user, something went wrong!"
                raise Exception()
            else:
                success = "Message sent to the user successfully"
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource='message/SendMessage')

    return render_template('message.html', receiver=receiver, error=error, success=success)


@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    global LoggedUser
    error = None
    success = None

    if request.method == 'POST':
        # get the entries from the form
        title: str = request.form.get('title')
        subject: str = request.form.get('subject')
        content: str = request.form.get('content')

        # now create a post object and push to database
        try:
            post: Post = Post(
                Id=PostModelHelper.CreatePostId(),
                PosterId=LoggedUser.Id,
                PosterFullName=LoggedUser.FirstName + " " + LoggedUser.LastName,
                PosterUsername=LoggedUser.Username,
                Subject=subject,
                Title=title,
                Content=content,
                PostDate=datetime.now()
            )
            operationResult: bool = PostDBActions.UpdatePost(post=post)
            if operationResult == False:
                error = "Could not create the post, something went wrong!"
                raise Exception()
            else:
                success = "Created the post successfully"
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource='create_post/UpdatePost')

    return render_template('create_post.html', error=error, success=success)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact_us', methods=['POST', 'GET'])
def contact_us():

    if request.method == 'POST':
        fullName: str = request.form.get('full-name')
        print(fullName)
        email: str = request.form.get('email')
        print(email)
        comment: str = request.form.get('comment')

        # now send an automated email to the server with the comments
        message = EmailMessage()
        message['Subject'] = f"New Contact Us Comments: {email}"
        message['To'] = "networkeremailserver@gmail.com"
        message['From'] = email
        message.set_content(f"New Contact Us form submitted by {fullName}: \n{comment}")
        # email_server.send_message(message)

    return render_template('contact_us.html')


@app.route('/terms_of_use')
def terms_of_use():
    return render_template('terms_of_use.html')


# run of the app
if __name__ == '__main__':
    app.run(debug = True)