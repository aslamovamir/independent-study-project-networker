import hashlib


class JobModelHelper:

    # helper method to create an id encrypted for the Job class
    def CreateJobID(title: str, employer: str, industry: str, description: str, location: str, salary: str) -> str:
        return hashlib.sha256(str.encode(title.join(employer).join(industry).join(description).join(location).join(salary))).hexdigest()