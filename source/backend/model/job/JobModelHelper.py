import hashlib


class JobModelHelper:

    # helper method to create an id encrypted for the Job class
    def CreateJobID(title: str, employer: str, description: str, location: str, salary: str) -> str:
        return hashlib.sha256(str.encode(title.join(employer).join(description).join(location).join(salary))).hexdigest()