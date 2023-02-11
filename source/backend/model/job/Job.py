from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Job:
    Id: str
    Title: str
    Employer: str
    Industry: str
    Description: str
    Location: str
    Salary: str
    PosterId: str
    DateCreated: datetime = field(default_factory=datetime.now)

     # Hydrates a Job entity using a pyrebase response value and returns it.
    def HydrateJob(job):
        return Job(
                Id = JobHydrator.HydrateProp(job, "Id"),
                Title = JobHydrator.HydrateProp(job, "Title"),
                Employer = JobHydrator.HydrateProp(job, "Employer"),
                Industry = JobHydrator.HydrateProp(job, "Industry"),
                Description = JobHydrator.HydrateProp(job, "Description"),
                Location = JobHydrator.HydrateProp(job, "Location"),
                Salary = JobHydrator.HydrateProp(job, "Salary"),
                PosterId = JobHydrator.HydrateProp(job, "PosterId"),
                DateCreated = JobHydrator.HydrateProp(job, "DateCreated")
            )


    # Converts this entity into a dictionary.
    def JobToDict(self) -> dict:
        return {
            'Id': str(self.Id),
            'Title': str(self.Title),
            'Employer': str(self.Employer),
            'Industry': str(self.Industry),
            'Description': str(self.Description),
            'Location': str(self.Location),
            'Salary': str(self.Salary),
            'PosterId': str(self.PosterId),
            'DateCreated': str(self.DateCreated)
        }

class JobHydrator:


    # A dictionary to maintain the Job entity's property name (key) and its type (value).
    _jobAttributes: dict[str, str] = {
        "Id": "str",
        "Title": "str",
        "Employer": "str",
        "Industry": "str",
        "Description": "str",
        "Location": "str",
        "Salary": "str",
        "PosterId": "str",
        "DateCreated": "datetime"
    }


    # Hydrates an individual property for the Job entity.
    def HydrateProp(job, prop: str):
        if prop not in JobHydrator._jobAttributes.keys():
            raise Exception(f"Property {prop} not defined for entity: Job")
        
        propType: str = JobHydrator._jobAttributes.get(prop)
        value = None
        
        try:
            pyreValue = job.val()[prop]
            value = JobHydrator.Cast(pyreValue, propType)
        except:
            value = JobHydrator.GetDefaultValue(prop)
        
        if value == None: raise Exception(f"Could not hydrate prop: {prop} for Job")
        
        return value


    # Handles conversion to a certain type.
    def Cast(pyreValue, propType):
        if propType == "datetime":
            datetimeValue: datetime = datetime.fromisoformat(pyreValue)
            return datetimeValue

        return pyreValue

        
    # Gets the default value for a property on the Job entity based on its type.
    def GetDefaultValue(prop: str):
        propType: str = JobHydrator._jobAttributes.get(prop)

        if propType == "str": return ""
        if propType == "datetime": return datetime.min
        else: return None