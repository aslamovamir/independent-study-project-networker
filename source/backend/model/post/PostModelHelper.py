import datetime


class PostModelHelper:

    # method to create a unique post Id
    def CreatePostId() -> int:
        return int(datetime.datetime.now().timestamp())