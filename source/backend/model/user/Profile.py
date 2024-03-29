from dataclasses import dataclass, field

@dataclass
class Experience:
    Title: str = ""
    Employer: str = ""
    DateStarted: str = ""
    DateEnded: str = ""
    Location: str = ""
    Description: str = ""

    def ExpToDict(self):
        return{
            'Title': str(self.Title),
            'Employer': str(self.Employer),
            'DateStarted': str(self.DateStarted),
            'DateEnded': str(self.DateEnded),
            'Location': str(self.Location),
            'Description': str(self.Description)
        }

    # converts a dictionary pyrebase response to experience object
    def HydrateExperience(ExperienceDict):
        return Experience(
            Title=ExperienceDict['Title'],
            Employer=ExperienceDict['Employer'],
            DateStarted=ExperienceDict['DateStarted'],
            DateEnded=ExperienceDict['DateEnded'],
            Location=ExperienceDict['Location'],
            Description=ExperienceDict['Description'],
        )

@dataclass
class Education:
    SchoolName: str = ""
    Degree: str = ""
    YearsAttended: int = 0

    def EducationToDict(self):
        return {
            'SchoolName': str(self.SchoolName),
            'Degree': str(self.Degree),
            'YearsAttended': int(self.YearsAttended)
        }

    # converts a dictionary pyrebase response to education object
    def HydrateEducation(EducationDict):
        return Education(
            SchoolName=EducationDict['SchoolName'],
            Degree=EducationDict['Degree'],
            YearsAttended=EducationDict['YearsAttended']
        )


@dataclass
class Profile:
    Title: str = "" 
    About: str = ""
    Gender: str = ""
    Ethnicity: str = ""
    DisabilityStatus: str = ""
    Location: str = ""
    PhoneNumber: str = "" 
    EducationList: list[Education] = field(default_factory=list)
    ExperienceList: list[Experience] = field(default_factory=list)

    def HydrateProfile(profile: dict):
        return Profile(
            Title = ProfileHydrator.HydrateProp(profile, "Title"),
            About = ProfileHydrator.HydrateProp(profile, "About"),
            Gender = ProfileHydrator.HydrateProp(profile, "Gender"),
            Ethnicity = ProfileHydrator.HydrateProp(profile, "Ethnicity"),
            DisabilityStatus = ProfileHydrator.HydrateProp(profile, "DisabilityStatus"),
            Location = ProfileHydrator.HydrateProp(profile, "Location"),
            PhoneNumber = ProfileHydrator.HydrateProp(profile, "PhoneNumber"),
            EducationList = ProfileHydrator.HydrateProp(profile, "EducationList"),
            ExperienceList = ProfileHydrator.HydrateProp(profile, "ExperienceList"),
        )

    def ProfileToDict(self):
        try:
            if self == None:
                self = Profile()
            
            if (self.EducationList == None):
                self.EducationList = []
            
            if (self.ExperienceList == None):
                self.ExperienceList = []

            return {
                'Title': str(self.Title),
                'About': str(self.About),
                'Gender': str(self.Gender),
                'Ethnicity': str(self.Ethnicity),
                'DisabilityStatus': str(self.DisabilityStatus),
                'Location': str(self.Location),
                'PhoneNumber': str(self.PhoneNumber),
                'EducationList': {i: self.EducationList[i].EducationToDict() for i in range(len(self.EducationList))},
                'ExperienceList': {i: self.ExperienceList[i].ExpToDict() for i in range(len(self.ExperienceList))}
            }
        except Exception as e:
            print(f"Could not convert a Profile entity to a dictionary object.\n{e}")


class ProfileHydrator:

    # A dictionary to maintain the Profile entity's property name (key) and its type (value).
    _profileAttributes: dict[str, str] = {
        "Title": "str",
        "About": "str",
        "Gender": "str",
        "Ethnicity": "str",
        "DisabilityStatus": "str",
        "Location": "str",
        "PhoneNumber": "str",
        "EducationList": "list[Education]",
        "ExperienceList": "list[Experience]"
    }

    # Hydrates an individual property for the Profile entity.
    def HydrateProp(profile: dict, prop: str):
        if prop not in ProfileHydrator._profileAttributes.keys():
            raise Exception(f"Property {prop} not defined for entity: Profile")
        
        propType: str = ProfileHydrator._profileAttributes.get(prop)
        value = None
        
        try:
            pyreValue = profile[prop]
            value = ProfileHydrator.CastComplexType(pyreValue, propType)
        except:
            value = ProfileHydrator.GetDefaultValue(prop)
        
        if value == None: raise Exception(f"Could not hydrate prop: {prop} for Profile")
        
        return value
    
    # Handles conversion to a complex type.
    def CastComplexType(pyreValue, propType):
        if propType == "list[Education]":
            educationList: list[Education] = []
            for education in pyreValue:
                educationList.append(Education.HydrateEducation(education))
            return educationList
        
        if propType == "list[Experience]":
            experienceList: list[Experience] = []
            for experience in pyreValue:
                experienceList.append(Experience.HydrateExperience(experience))
            return experienceList

        return pyreValue
    
    # Gets the default value for a property on the Profile entity based on its type.
    def GetDefaultValue(prop: str):
        propType: str = ProfileHydrator._profileAttributes.get(prop)

        if propType == "str": return ""
        elif propType == "bool": return True
        elif propType == "list[Education]": return []
        elif propType == "list[Experience]": return []
        else: return None