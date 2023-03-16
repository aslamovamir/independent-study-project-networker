from backend.firebase.Firebase import database
from backend.model.post.Post import Post
from backend.helpers.MenuHelper import MenuHelper
from datetime import datetime


class PostDBActions:

    # method to update the post entity node in the database
    def UpdatePost(post: Post, collection: str = "Posts") -> bool:
        try:
            database.child(collection).child(post.Id).set(post.PostToDict())
            return True
        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource="PostDbActions/UpdatePost")

    
    # method to fetch all posts
    def GetAllPosts(collection: str = "Posts") -> list[Post]:
        try:
            response = database.child(collection).get()
            if response == None: return None

            responseListed: list = response.each()
            if (responseListed == None): return None
            posts: list[Post] = []
            for post in responseListed:
                if post == None: continue
                else: posts.append(Post.HydratePost(post))

            return posts
        except:
            return None