from backend.model.job.Job import Job
from backend.firebase.Firebase import database
from backend.helpers.MenuHelper import MenuHelper


class JobDBActions:

    # method to update the job entity node in the database
    def UpdateJob(job: Job, collection: str = "Jobs") -> bool:
        try:
            database.child(collection).child(job.Id).set(job.JobToDict())
            return True
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource="JobrDBActions:UpdateJob")

    
    # method to retun as a list all the jobs in the database
    def GetAllJobs(collection: str = "Jobs") -> list[Job]:
        try:
            jobsResponse = database.child(collection).get()

            if jobsResponse == None: return None
            
            jobsResponseList: list = jobsResponse.each()
            if (jobsResponseList == None): return None 
            
            jobs: list[Job] = []
            for job in jobsResponse.each():
                if job == None: continue
                else: jobs.append(Job.HydrateJob(job))

            return jobs
        except:
            return None
        

    # method to return the list of all jobs not created by a user
    def GetAllJobsOffUser(userId: str, collection: str = "Jobs") -> list[Job]:
        try:
            jobsResponse = database.child(collection).get()

            if jobsResponse == None: return None
            
            jobsResponseList: list = jobsResponse.each()
            if (jobsResponseList == None): return None 
            
            jobs: list[Job] = []
            for job in jobsResponse.each():
                if job == None: continue
                else:
                    if job.val()['PosterId'] != userId: 
                        jobs.append(Job.HydrateJob(job))

            return jobs
        except:
            return None
        
    
    # method to retun as a list all the jobs created by a user in the database
    def GetAllJobsUser(userId: str, collection: str = "Jobs") -> list[Job]:
        print("In Get All Jobs User")
        try:
            jobsResponse = database.child(collection).get()

            if jobsResponse == None: return None
            
            jobsResponseList: list = jobsResponse.each()
            if (jobsResponseList == None): return None 
            
            jobs: list[Job] = []
            for job in jobsResponse.each():
                if job == None: continue
                else:
                    if job.val()['PosterId'] == userId:
                        jobs.append(Job.HydrateJob(job))

            return jobs
        except:
            return None