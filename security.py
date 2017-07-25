users = [
    {
        'id': 1,
        'username': 'bob',
        'password'
    }
]

username_mapping = { 'bob': {
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
}

userid_mapping = { 1: {
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    # could be also username_mapping['username'] but .get give us option to include also the default value - None
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
