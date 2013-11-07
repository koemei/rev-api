import requests

def _rev_auth_str(client_api_key, user_api_key):
    """Returns a Rev Auth string."""

    return 'Rev %s:%s' % (client_api_key, user_api_key)


class RevAuth(requests.auth.AuthBase):
    """
    Custom authorization for Rev API
    See http://www.rev.com/api/security
    Format:
        Authorization: Rev [ClientAPIKey]:[UserAPIKey]
    """

    def __init__(self, client_api_key, user_api_key):
        self._client_api_key = client_api_key
        self._user_api_key = user_api_key

    def __call__(self, r):
        r.headers['Authorization'] = _rev_auth_str(self._client_api_key, self._user_api_key)
        return r