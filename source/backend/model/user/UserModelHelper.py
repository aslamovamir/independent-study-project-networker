import hashlib


class UserModelHelper:

    # helper method to create a user id encrypted for the User class
    # we never statically store the password of the user for security purposes - instead, we hash password with username and pass it as ID
    def CreateUserID(username: str, password: str) -> str:
        return hashlib.sha256(str.encode(username.join(password))).hexdigest()