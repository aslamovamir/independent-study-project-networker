import datetime
from backend.model.message.Message import Message
from backend.firebase.Firebase import database
from backend.model.user.User import User
from backend.database.UserDBActions import UserDBActions

class MessageHelpers:
    
    # Converts a message entity into a dictionary.
    def MessageToDict(message: Message) -> dict:
        return {
            'Id': str(message.Id),
            'SenderId': str(message.SenderId),
            'ReceiverId': str(message.ReceiverId),
            'Content': str(message.Content),
            'IsRead': str(message.IsRead)
        }


    # Checks if the specified message exists in the DB using the provided ID.
    def MessageExists(messageId: int, collection: str = "Messages") -> bool:
        return False if MessageHelpers.GetMessageById(
            messageId, collection) == None else True


    # Creates a message id which is essentially its index.
    # Example: If total messages => 4 then messageId => 5.
    def CreateMessageId(collection: str = "Messages") -> int:
        return int(datetime.datetime.now().timestamp())


    # Gets a PyreResponse of all messages from the DB and returns
    # a list of message entities after constructing it.
    def GetAllMessages(collection: str = "Messages") -> list[Message]:
        try:
            messagesResponse = database.child(collection).get()
            if messagesResponse == None: return None

            messagesResponseList: list = messagesResponse.each()
            if (messagesResponseList == None): return None

            messages: list[Message] = []
            for message in messagesResponseList:
                if message == None: continue
                else: messages.append(Message.HydrateMessage(message))

            return messages

        except:
            return None


    # Gets a specific Message from the database based on the Message ID provided.
    def GetMessageById(messageId: int, collection: str = "Messages") -> Message:
        try:
            message: Message = Message.HydrateMessage(
                database.child(collection).child(messageId).get())
            
            if message == None: raise Exception()

            return message

        except Exception as e:
            print(f"Could not get the specified message with ID: {messageId}\n{e}")
    

    # Deletes a specific Message from the database based on the Message ID provided.
    def DeleteMessageById(messageId: int, collection: str = "Messages") -> bool:
        try:
            if not MessageHelpers.MessageExists(messageId, collection):
                return False
            
            database.child(collection).child(messageId).remove()
            print("Message deleted successfully.")
            return True

        except:
            return False


    # Deletes all messages from a particular user to a particular user
    def DeleteMessagesBySenderReceiverID(sender: User, receiver: User, collection: str = "Messages") -> bool:
        try:
            allMessages: list[Message] = MessageHelpers.GetAllMessages(collection=collection)
            if allMessages == None or allMessages == []:
                return False

            for message in allMessages:
                if message.SenderId == sender.Id and message.ReceiverId == receiver.Id:
                    database.child(collection).child(message.Id).remove()
            
            print("Message(s) deleted successfully.")
            return True
        except Exception as e:
            print(f"\nFailure! Could not delete messages by a sender to a receiver for some reason: {e}\n")
            return False


    # Creates or updates the specified message in the DB.
    # Returns true if update was successful else false.
    def UpdateMessage(message: Message, collection: str = "Messages", userCollection: str = "Users") -> bool:
        try:
            database.child(collection).child(message.Id).set(
                MessageHelpers.MessageToDict(message))
            
            return True

        except Exception as e:
            print(f"Could not update message with ID: {message.Id}\n{e}")
            return False
    

    # Gets all the received messages of the specified user.
    def GetAllReceivedMessages(
        userId: str,
        onlyUnread: bool = False,
        messageCollection: str = "Messages") -> list[Message]:

        allMessages: list[Message] = MessageHelpers.GetAllMessages(messageCollection)
        if allMessages == None: return None

        # Filter all messages where the receiver id is equal to the specified user id.
        allMessagesReceived: list[Message] = list(filter(
            lambda m: m.ReceiverId == userId, allMessages))
        
        if onlyUnread:
            allMessagesReceived = list(filter(
                lambda m: m.ReceiverId == userId and not m.IsRead, allMessages))

        return allMessagesReceived


    # Sends a message using the specified sender and receiver.
    def SendMessage(
        senderId: str,
        receiverId: str,
        messageCollection: str = "Messages",
        userCollection: str = "Users") -> bool:

        try:

            receiverName: User = UserDBActions.GetUserById(receiverId, userCollection).FirstName
            
            content: str = str(
                input(f"\nEnter the content for the message to {receiverName}:\n\n"))
            
            messageSent: bool = MessageHelpers.UpdateMessage(Message(
                        MessageHelpers.CreateMessageId(),
                        senderId,
                        receiverId,
                        content),
                        messageCollection)
            
            if not messageSent: raise Exception()

            if messageSent: print(f"\nMessage sent to {receiverName} successfully.")

            return messageSent
            
        except Exception as e:
            print(f"\nException occurred. Message could not be sent.\n{e}")
            return False