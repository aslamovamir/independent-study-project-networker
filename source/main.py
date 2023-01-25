from helpers.MenuHelper import MenuHelper
from actions.DisplayAboutApp import DisplayAboutApp


class Main:

    # entry
    # menu options for the user
    menuOptions: list[str] = [
        "About Networker",
        "Log In",
        "Sign Up",]

    print("\nWelcome to Networker!")
    while True:
        try:
            MenuHelper.RequestInput()
            # display menu options to the user
            MenuHelper.DisplayMenuOptions(options=menuOptions)

            # now take in the menu option entered by the user
            decision: int = MenuHelper.InputOption()
            
            # check the menu option selected and redirect the user correspondingly
            if decision == 1:
                MenuHelper.DisplaySelectedOption(selectedOption=menuOptions[decision-1])
                DisplayAboutApp()

            elif decision == 2:
                MenuHelper.DisplaySelectedOption(selectedOption=menuOptions[decision-1])

            elif decision == 3:
                MenuHelper.DisplaySelectedOption(selectedOption=menuOptions[decision-1])
            
            elif decision == -1:
                MenuHelper.InformMenuQuit()
                break

            else:
                MenuHelper.WarnInvalidInput()

        except:
            MenuHelper.WarnInvalidInput()
