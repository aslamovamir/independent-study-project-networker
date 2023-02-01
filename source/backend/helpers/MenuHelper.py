

# class for MenuHelper
class MenuHelper:

    # prints an error message in case of exceptions and displays those exceptions
    def DisplayErrorException(exception: str, errorSource: str):
        print(f"\nFailure! Something went wrong for some reason. \nPlease address the following exception in {errorSource}: {exception}")