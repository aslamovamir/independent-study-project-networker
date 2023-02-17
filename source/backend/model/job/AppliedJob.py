from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AppliedJob:
    Id: str
    UserId: str
    PosterId: str
    UserName: str
    JobId: str
    JobTitle: str
    JobEmployer: str
    Status: str
    StartDate: str
    GoodFitReasoning: str
    SponsorshipRequirement: str
    DateApplied: datetime = field(default_factory=datetime.now)
    DateReviewed: datetime = field(default_factory=datetime.now)


    # hydrates an AppliedJob entity using a pyrebase response value and returns it
    def HydrateAppliedJob(appliedJob):
        return AppliedJob(
            Id = AppliedJobHydrator.HydrateProp(appliedJob, "Id"),
            UserId = AppliedJobHydrator.HydrateProp(appliedJob, "UserId"),
            PosterId = AppliedJobHydrator.HydrateProp(appliedJob, "PosterId"),
            UserName = AppliedJobHydrator.HydrateProp(appliedJob, "UserName"),
            JobId = AppliedJobHydrator.HydrateProp(appliedJob, "JobId"),
            JobTitle = AppliedJobHydrator.HydrateProp(appliedJob, "JobTitle"),
            JobEmployer = AppliedJobHydrator.HydrateProp(appliedJob, "JobEmployer"),
            Status = AppliedJobHydrator.HydrateProp(appliedJob, "Status"),
            StartDate = AppliedJobHydrator.HydrateProp(appliedJob, "StartDate"),
            GoodFitReasoning = AppliedJobHydrator.HydrateProp(appliedJob, "GoodFitReasoning"),
            SponsorshipRequirement = AppliedJobHydrator.HydrateProp(appliedJob, "SponsorshipRequirement"),
            DateApplied = AppliedJobHydrator.HydrateProp(appliedJob, "DateApplied"),
            DateReviewed = AppliedJobHydrator.HydrateProp(appliedJob, "DateReviewed")
        )


    # converts this entity into a dictionary
    def AppliedJobToDict(self) -> dict:
        return {
            'Id': str(self.Id),
            'UserId': str(self.UserId),
            'PosterId': str(self.PosterId),
            'UserName': str(self.UserName),
            'JobId': str(self.JobId),
            'JobTitle': str(self.JobTitle),
            'JobEmployer': str(self.JobEmployer),
            'Status': str(self.Status),
            'StartDate': str(self.StartDate),
            'GoodFitReasoning': str(self.GoodFitReasoning),
            'SponsorshipRequirement': str(self.SponsorshipRequirement),
            'DateApplied': str(self.DateApplied),
            'DateReviewed': str(self.DateReviewed)
        }


class AppliedJobHydrator:


    # A dictionary to maintain the AppliedJob entity's property name (key) and its type (value).
    _appliedJobAttributes: dict[str, str] = {
        "Id": "str",
        "UserId": "str",
        "PosterId": "str",
        "UserName": "str",
        "JobId": "str",
        "JobTitle": "str",
        "JobEmployer": "str",
        "Status": "str",
        "StartDate": "str",
        "GoodFitReasoning": "str",
        "SponsorshipRequirement": "str",
        "DateApplied": "datetime",
        "DateReviewed": "datetime"
    }


    # Hydrates an individual property for the AppliedJob entity.
    def HydrateProp(appliedJob, prop: str):
        if prop not in AppliedJobHydrator._appliedJobAttributes.keys():
            raise Exception(f"Property {prop} not defined for entity: AppliedJob")
        
        propType: str = AppliedJobHydrator._appliedJobAttributes.get(prop)
        value = None
        
        try:
            pyreValue = appliedJob.val()[prop]
            value = AppliedJobHydrator.Cast(pyreValue, propType)
        except:
            value = AppliedJobHydrator.GetDefaultValue(prop)
        
        if value == None: raise Exception(f"Could not hydrate prop: {prop} for AppliedJob")
        
        return value


    # Handles conversion to a certain type.
    def Cast(pyreValue, propType):
        if propType == "datetime":
            datetimeValue: datetime = datetime.fromisoformat(pyreValue)
            return datetimeValue

        return pyreValue


    # Gets the default value for a property on the AppliedJob entity based on its type.
    def GetDefaultValue(prop: str):
        propType: str = AppliedJobHydrator._appliedJobAttributes.get(prop)

        if propType == "str": return ""
        if propType == "datetime": return datetime.min
        else: return None