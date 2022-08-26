def get_data(session: dict) -> dict:
    if 'user_id' in session:
        return {
            'user_logged': True,
            'user_id': session['user_id']
        }
    else:
        return {
            'user_logged': False
        }
