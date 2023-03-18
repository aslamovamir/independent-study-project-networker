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
        

    # method to fetch a post by its Id
    def GetPostById(postId: str, collection: str = "Posts") -> Post:
        try:
            post: Post = Post.HydratePost(
                database.child(collection).child(postId).get())
            
            if post == None:
                raise Exception(
                    f"Could not get the specified post with ID: {postId}")
            
            return post
        except:
            print(f"Could not get the specified post with ID: {postId}")

    
    # method to like or dislike a post
    def Evaluate(userId: str, post: Post, like: bool, collection: str = "Posts") -> bool:
        try:
            if like:
                if userId not in post.LikesDislikes:
                    post.LikesDislikes[userId] = True
                    post.NumberLikes += 1
                    newDict = post.LikesDislikes
                    database.child(collection).child(post.Id).set(post.PostToDict())
                    database.child(collection).child(post.Id).child("LikesDislikes").set(newDict)
                elif userId in post.LikesDislikes and post.LikesDislikes[userId] == False:
                    post.LikesDislikes[userId] = True
                    post.NumberLikes += 1
                    post.NumberDislikes -= 1
                    newDict = post.LikesDislikes
                    database.child(collection).child(post.Id).set(post.PostToDict())
                    database.child(collection).child(post.Id).child("LikesDislikes").set(newDict)
            else:
                if userId not in post.LikesDislikes: 
                    post.LikesDislikes[userId] = False
                    post.NumberDislikes += 1
                    newDict = post.LikesDislikes
                    database.child(collection).child(post.Id).set(post.PostToDict())
                    database.child(collection).child(post.Id).child("LikesDislikes").set(newDict)
                elif userId in post.LikesDislikes and post.LikesDislikes[userId] == True:
                    post.LikesDislikes[userId] = False
                    post.NumberDislikes += 1
                    post.NumberLikes -= 1
                    newDict = post.LikesDislikes
                    database.child(collection).child(post.Id).set(post.PostToDict())
                    database.child(collection).child(post.Id).child("LikesDislikes").set(newDict)

            return True

        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource='PostDBActions/Evaluate')
            return False
        

    # method to add a comment to a post
    def Comment(user: str, post: Post, comment: str, collection: str = "Posts") -> bool:
        try:
            if user not in post.Comments:
                post.Comments[user] = comment
                newDict = post.Comments
                post.NumberComments += 1
                database.child(collection).child(post.Id).set(post.PostToDict())
                database.child(collection).child(post.Id).child("Comments").set(newDict)
            else:
                post.Comments[user] += "\n"
                post.Comments[user] += comment
                newDict = post.Comments
                database.child(collection).child(post.Id).child("Comments").set(newDict)

            return True

        except Exception as e:
            MenuHelper.DisplayErrorException(exception=e, errorSource='PostDBActions/Comment')
            return False