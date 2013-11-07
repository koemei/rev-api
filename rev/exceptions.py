
class SettingsFileNotFoundError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)