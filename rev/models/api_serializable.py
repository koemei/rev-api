
class ApiSerializable(object):
    """
    This is the base class for model objects initialized with a json api response
    """

    def __init__(self, fields=None):
        if fields is not None:
            for field_name in fields:
                setattr(self, field_name, fields[field_name])