import jwt

def encode_password(password, secret):
    password = jwt.encode({'payload':password}, secret, algorithm='HS256')
    return str(password)


def decode_password(password, secret):
    password = jwt.decode(password, secret, algorithms=['HS256'])
    return password['payload']


def check_password(password1, password2, secret):
    password1 = decode_password(password1, secret)
    print(password1, password2)
    return password1 == password2
