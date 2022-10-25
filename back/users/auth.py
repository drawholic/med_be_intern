import os
from dotenv import load_dotenv
import jwt
from .exceptions import BadTokenException


def get_env() -> dict:
    load_dotenv()
    env = {'DOMAIN':os.getenv('DOMAIN'),
            "AUDIENCE":os.getenv('AUDIENCE'),
            'ISSUER':os.getenv('ISSUER'),
            'ALGORITHMS':os.getenv('ALGORITHMS'),
            'SECRET':os.getenv('SECRET')
            }
    return env


def token_generate(payload: str) -> str:
    load_dotenv()
    secret = os.getenv('SECRET')
    token = jwt.encode({"payload": payload}, secret, algorithm='HS256')
    
    return token


def token_decode(token: str):
    load_dotenv()
    secret = os.getenv('SECRET')
    try:
        result = jwt.decode(token.credentials, secret, algorithms=['HS256'])['payload']
        print(result, 'result')
        return result 
    except Exception:
        raise BadTokenException
            


class AuthToken():

    def __init__(self, token):
        self.token = token
        self.config = get_env()

        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        return payload


