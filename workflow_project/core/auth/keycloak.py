from jose import jwt
import requests

KEYCLOAK_CONFIG_URL = 'http://localhost:8080/realms/demo-realm/.well-known/openid-configuration'
KEYCLOAK_CLIENT_ID = 'django-backend'
ALGORITHMS = ['RS256']

def get_public_key():
    config = requests.get(KEYCLOAK_CONFIG_URL).json()
    jwks_uri = config["jwks_uri"]
    jwks = requests.get(jwks_uri).json()
    return jwks["keys"][0]  # Use the first public key

def decode_token(token):
    key = get_public_key()
    return jwt.decode(token, key, algorithms=ALGORITHMS, audience="account")