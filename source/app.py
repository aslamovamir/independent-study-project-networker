from flask import Flask, render_template, session, request, redirect, flash, url_for
from backend.helpers.AuthenticationHelper import AuthenticationHelper
from backend.model.user.User import User
from backend.model.user.Profile import Profile
from backend.model.job.Job import Job
from backend.model.job.AppliedJob import AppliedJob
from backend.model.job.JobModelHelper import JobModelHelper
from backend.model.user.UserModelHelper import UserModelHelper
from backend.database.UserDBActions import UserDBActions
from backend.database.JobDBActions import JobDBActions
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
                    ))

                    if operationResult == False: raise Exception()
                    else: flash("Success: You have successfully signed up.")
                except Exception as e:
                    MenuHelper.DisplayErrorException(exception=e, errorSource="signup:UpdateUser")
            else:
                error = "Invalid password."
        else:
            error = "This username already exists."

    return render_template('signup.html', error=error)


@app.route('/dashboard')
def dashboard():
    global LoggedUser
    return render_template('dashboard.html', loggedUser=LoggedUser)


@app.route('/update_profile', methods=['POST', 'GET'])
def update_profile():
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
            if operationResult == False: raise Exception()
            else: return render_template('dashboard.html', loggedUser=LoggedUser)
        except Exception as e:
                    MenuHelper.DisplayErrorException(exception=e, errorSource="update_profile:UpdateUser")

    return render_template('update_profile.html', loggedUser=LoggedUser)


@app.route('/create_job_posting', methods=['POST', 'GET'])
def create_job_posting():
    global LoggedUser

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

            if operationResult == False: raise Exception()
            else: return render_template('dashboard.html', loggedUser=LoggedUser)

        except Exception as e:
                    MenuHelper.DisplayErrorException(exception=e, errorSource="create_job_posting:CreateJobID")


    return render_template('create_job_posting.html', loggedUser=LoggedUser)


@app.route('/apply_for_job', methods=['POST', 'GET'])
def apply_for_job():
    global LoggedUser


    # get all the jobs created by others
    jobs: list[Job] = []
    try:
        jobs = JobDBActions.GetAllJobsOffUser(userId=LoggedUser.Id)
        if jobs == None:
            jobs = []
    except Exception as e:
        MenuHelper.DisplayErrorException(exception=e, errorSource="apply_for_job:GetAllJobsOffUser")

    if request.method == 'POST':
        # get the id of the job clicked by the user via the button assigned to it
        jobIdToApply: str = request.form['applyBtn']
        # now check if the user already applied for this job
        try:
            if JobDBActions.CheckIfApplied(userId=LoggedUser.Id, jobId=jobIdToApply):
                error = "You have already applied for this job."
                return render_template('apply_for_job.html', jobs=jobs, error=error)
        except Exception as e:
            MenuHelper.DisplayErrorException(errorSource='apply_for_job:CheckIfApplied')
        # get the job
        for job in jobs:
            if job.Id == jobIdToApply:
                jobToApply: Job = job
        # now redirect to a new application page, with the job id and the logged user
        return render_template('application.html', job=jobToApply)

    return render_template('apply_for_job.html', jobs=jobs)


@app.route('/application', methods=['POST', 'GET'])
def application():

    global LoggedUser
    error = None

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

            if operationResult == False: raise Exception()
            else: return render_template('dashboard.html', loggedUser=LoggedUser)
            
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource='application:JobDBActions:UpdateAppliedJob')

    return render_template('dashboard.html', loggedUser=LoggedUser)


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
                if operationResult == False: raise Exception()
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
                if operationResult == False: raise Exception()
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

    return render_template('review_applications.html', jobs=jobsPosted)


@app.route('/my_network', methods=['POST', 'GET'])
def my_network():
    global LoggedUser

    # get all the users except for the logged user
    users: list[User] = []
    try:
        users = UserDBActions.GetAllUsersOffUser(userId=LoggedUser.Id)
        if users == None:
            users = []
    except Exception as e:
        MenuHelper.DisplayErrorException(exception=e, errorSource='my_network/GetAllUsersOffUser')

    return render_template('my_network.html', users=users)



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