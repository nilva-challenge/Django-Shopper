"""
    the latter functions to exchange google javascript client id token for user information
"""


def authorize_by_google_api_profile(client_id, token):
    from google.oauth2 import id_token
    from google.auth.transport import requests

    try:
        idinfo = None
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        # userid = idinfo['sub']

    except ValueError as er:
        # Invalid token
        print('authorize_by_google_api_profile: ', er)
        return None

    return idinfo