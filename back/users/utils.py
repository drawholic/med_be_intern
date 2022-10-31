
import os
from dotenv import load_dotenv 
import jwt


def check_password(password, user_password):
    load_dotenv()
    secret = os.getenv('SECRET')
    decode = jwt.decode(user_password, secret, algorithms=['HS256'])['payload']
    return decode == password


def encode_password(password):
    load_dotenv()
    secret = os.getenv('SECRET')
    return jwt.encode({'payload': password}, secret, algorithm='HS256')


def decode_password(password, secret):
    password = jwt.decode(password, secret, algorithms=['HS256'])
    return password['payload']

