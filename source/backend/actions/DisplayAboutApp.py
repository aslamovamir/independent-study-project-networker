from helpers.MenuHelper import MenuHelper


def DisplayAboutApp() -> None:
    # basic info
    MenuHelper.DefineSectionBreak()
    print("\nWelcome to Networker!",
        "\n\n© Networker is an app designed to help users better network with each other.",
        "\nSpecifically, it helps them interchange their profiles with others, send friend requests,",
        "stay connected, and send text messages. \nIt also helps them post job postings and have ",
        "others apply for them. Users can also post on any topic and others with relevant interest",
        "\nget notified.")
    # copyright
    MenuHelper.DisplayCopyright()
    MenuHelper.DefineSectionBreak()