from backend.model.job.Job import Job
from backend.model.job.AppliedJob import AppliedJob
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
        
    
    # method to get Job object by job id
    def GetJobFromId(jobId: str, collection: str = "Jobs") -> Job:
        try:
            jobsResponse = database.child(collection).get()

            if jobsResponse == None: return None
            
            jobsResponseList: list = jobsResponse.each()
            if (jobsResponseList == None): return None 
            
            for job in jobsResponse.each():
                if job == None: continue
                else:
                    if job.val()['Id'] == jobId:
                        return Job.HydrateJob(job)

            return None
        except:
            return None
        
    
    # method to update the applied job entity node in the database
    def UpdateAppliedJob(appliedJob: AppliedJob, collection: str = "AppliedJobs") -> bool:
        try:
            # the id of the applied job entry is the combination of user id and job id
            database.child(collection).child(appliedJob.UserId + appliedJob.JobId).set(appliedJob.AppliedJobToDict())
            return True
        except Exception as e:
            MenuHelper.DisplayErrorException(errorSource="JobDBActions:UpdateAppliedJob")


    # method to check if the user has already applied for a job
    def CheckIfApplied(userId: str, jobId: str, collection: str = "AppliedJobs") -> bool:
        try:
            jobsResponse = database.child(collection).get()

            if jobsResponse == None: return None
            
            jobsResponseList: list = jobsResponse.each()
            if (jobsResponseList == None): return None 
            
            for job in jobsResponse.each():
                if job == None: continue
                else:
                    if job.val()['UserId'] == userId and job.val()['JobId'] == jobId:
                        return True

            return False
        except:
            return False