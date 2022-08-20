import google_auth_oauthlib.flow
from google.oauth2 import credentials
from google_auth_oauthlib import flow


client_secret_file = ''
auth_redirect_domain = ''


def get_login_url():

    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(client_secret_file,
                                                                   scopes=['email'])

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow.redirect_uri = 'http://127.0.0.1:8000/login'

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='online',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true',

        hd='sonline20.sen.go.kr',
        prompt='select_account'
    )

    return authorization_url, state
