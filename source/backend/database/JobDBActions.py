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