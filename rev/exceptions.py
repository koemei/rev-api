
class SettingsFileNotFoundError(Exception):
    """
    Settings file was not found
    """

    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)


class OrderNotFoundError(Exception):
    """
    Order with a given external ref was not found on rev api
    """

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)