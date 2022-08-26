import requests

LOGIN_URL = 'https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
EMAIL_URL = 'https://openidconnect.googleapis.com/v1/userinfo'

CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://127.0.0.1:8000/account/auth'
SCOPE = 'openid email'


def get_login_url() -> str:
    return f'{LOGIN_URL}&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}'


def token_request(code: str) -> requests.Response:
    return requests.post(TOKEN_URL, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code,
        'grant_type': 'authorization_code'
    })


def email_request(token: str) -> requests.Response:
    return requests.get(f'{EMAIL_URL}', headers={
        'Authorization': f'Bearer {token}'
    })


def get_email(code: str) -> str:
    token_response = token_request(code)
    token_json = token_response.json()
    token = token_json['access_token']

    email_response = email_request(token)
    email_json = email_response.json()
    print(email_json)
    return email_json['email']
