

def passwords_match(user):
    if user['password'] == user['confirm_password']:
        return True

    else: 
        return False
