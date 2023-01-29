

# class for MenuHelper
class MenuHelper:

    # helps to print a line to distinguish between different sections in program
    def DefineSectionBreak():
        print("------------------------------------------------------------------------------------------------------------------------------------------------")
    

    # takes in a list of otions and prints in a formatted way
    def DisplayMenuOptions(options: list[str]):
        i: int = 1
        for option in options:
            print(f"{i} - {option}")
            i += 1

    
    # gives the user general instruction to select a menu option
    def RequestInput():
        print("\nPlease select an option to continue:")

    
    # informs the user that they decided to quit a menu selection
    def InformMenuQuit():
        print("\nYou have selected to Quit.\n")


    # inputs the menu option number from the user
    def InputOption() -> int:
        return int(input("Enter (-1 to Quit): "))

    
    # inputs a string stream
    def InputStream() -> str:
        return input("Enter (-1 to Quit): ")

    
    # displays the menu option selected for confirmation purposes
    def DisplaySelectedOption(selectedOption: str):
        print("Selected: ", selectedOption)


    # displays an error message that entered input is invalid
    def WarnInvalidInput():
        print("\nError! Invalid Entry! Please try again.")

    
    # informs of successful operation completion to the user
    def InformSuccessOperation():
        print("\nSuccess! Operation successfully completed.\n")

    
    # informs of unseccessful operation completion to the user
    def InformFailureOperation():
        print("\nFalure! Operation unsuccessfully completed.\n")


    # prints an error message in case of exceptions and displays those exceptions
    def DisplayErrorException(exception: str, errorSource: str):
        print(f"\nFailure! Something went wrong for some reason. \nPlease address the following exception in {errorSource}: {exception}")

    
    # prints the copyright information
    def DisplayCopyright():
        print("\n\nCopyright: © Networker, January 2023.\nEngineer: Amir Aslamov.\nAll rights reserved.\n")

    
    # validates that input is not empty
    def ValidateEmptyInput(input: str) -> bool:
        return len(input) == 0

    
    # asks the user for change confirmation
    def ConfirmChanges() -> bool:
        if input("\nWould you like to save changes? Y/N: ") == "Y":
            return True
        else:
            return False