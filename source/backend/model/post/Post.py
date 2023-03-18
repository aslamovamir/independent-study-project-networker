from dataclasses import dataclass, field
from datetime import datetime
from backend.helpers.MenuHelper import MenuHelper


# post entity
@dataclass
class Post:
    Id: str
    PosterId: str
    PosterFullName: str
    PosterUsername: str
    Subject: str
    Title: str
    Content: str
    LikesDislikes: dict[str, bool] = field(default_factory=dict)
    Comments: dict[str, str] = field(default_factory=dict)
    PostDate: datetime = field(default_factory=datetime.now)
    NumberLikes: int = 0
    NumberDislikes: int = 0
    NumberComments: int = 0

    # hydrates the post entity using a pyrebase response value and returns it
    def HydratePost(post):
        return Post(
            Id = PostHydrator.HydrateProp(post, "Id"),
            PosterId = PostHydrator.HydrateProp(post, "PosterId"),
            PosterFullName = PostHydrator.HydrateProp(post, "PosterFullName"),
            PosterUsername = PostHydrator.HydrateProp(post, "PosterUsername"),
            Subject = PostHydrator.HydrateProp(post, "Subject"),
            Title = PostHydrator.HydrateProp(post, "Title"),
            Content = PostHydrator.HydrateProp(post, "Content"),
            LikesDislikes = PostHydrator.HydrateProp(post, "LikesDislikes"),
            Comments = PostHydrator.HydrateProp(post, "Comments"),
            PostDate = PostHydrator.HydrateProp(post, "PostDate"),
            NumberLikes = PostHydrator.HydrateProp(post, "NumberLikes"),
            NumberDislikes = PostHydrator.HydrateProp(post, "NumberDislikes"),
            NumberComments = PostHydrator.HydrateProp(post, "NumberComments")
        )
    
    # method to convert post object to a dictionary
    def PostToDict(self) -> dict[str, str]:
        try:
            return {
                'Id': str(self.Id),
                'PosterId': str(self.PosterId),
                'PosterFullName': str(self.PosterFullName),
                'PosterUsername': str(self.PosterUsername),
                'Subject': str(self.Subject),
                'Title': str(self.Title),
                'Content': str(self.Content),
                'LikesDislikes': self.LikesDislikes,
                'Comments': self.Comments,
                'PostDate': str(self.PostDate),
                'NumberLikes': str(self.NumberLikes),
                'NumberDislikes': str(self.NumberDislikes),
                'NumberComments': str(self.NumberComments)
            }
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource="Post/PostToDict")

    

class PostHydrator:
    
    # a dictionary to maintain the Post entity's property name (key) and its type (value)
    _postAttributes: dict[str, str] = {
        "Id": "str",
        "PosterId": "str",
        "PosterFullName": "str",
        "PosterUsername": "str",
        "Subject": "str",
        "Title": "str",
        "Content": "str",
        "LikesDislikes": "dict[str, bool]",
        "Comments": "dict[str, str]",
        "PostDate": "datetime",
        "NumberLikes": "int",
        "NumberDislikes": "int",
        "NumberComments": "int"
    }


    # hydrates an individual property for the Post entity
    def HydrateProp(post, prop: str):
        if prop not in PostHydrator._postAttributes.keys():
            raise Exception(f"Property {prop} not defined for entity: Post")
        
        propType: str = PostHydrator._postAttributes.get(prop)
        value = None
        
        try:
            pyreValue = post.val()[prop]
            value = PostHydrator.Cast(pyreValue, propType)
        except:
            value = PostHydrator.GetDefaultValue(prop)
        
        if value == None: raise Exception(f"Could not hydrate prop: {prop} for Post")
        
        return value
    

    # Handles conversion to a certain type.
    def Cast(pyreValue, propType):
        
        if propType == "datetime":
            datetimeValue: datetime = datetime.fromisoformat(pyreValue)
            return datetimeValue
        
        return pyreValue
    

     # Gets the default value for a property on the User entity based on its type.
    def GetDefaultValue(prop: str):
        propType: str = PostHydrator._postAttributes.get(prop)

        if propType == "str": return ""
        elif propType == "int": return 0
        elif propType == "bool": return True
        elif propType == "dict[str, bool]": return {}
        elif propType == "dict[str, str]": return {}
        elif propType == "datetime": return datetime.min
        else: return None