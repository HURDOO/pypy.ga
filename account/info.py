USER_ID_KEY = 'account_user_id'
USER_LOGGED_KEY = 'account_user_logged'


def get_data(session: dict) -> dict:
    if USER_ID_KEY in session:
        return {
            USER_LOGGED_KEY: True,
            USER_ID_KEY: session[USER_ID_KEY]
        }
    else:
        return {
            USER_LOGGED_KEY: False
        }


def get_user_id(session: dict):
    if USER_ID_KEY in session:
        return session[USER_ID_KEY]
    else:
        return None
