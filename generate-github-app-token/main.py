from jwt import JWT
from jwt import jwk_from_pem 
import time
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Load your GitHub App's private key
with open('/path/to/your/private-key.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# Define constants
APP_ID = '123456'  # Replace with your GitHub App ID
INSTALLATION_ID = '12345678'  # Replace with your GitHub App Installation ID

# Create JWT
now = int(time.time())
payload = {
    "iat": now,             # Issued at time
    "exp": now + 600,       # JWT expiration time (10 minutes maximum)
    "iss": APP_ID           # GitHub App ID
}


# Create an instance of JWT
jwt_instance = JWT()

# Convert the private key to JWK format
private_key_jwk = jwk_from_pem(private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
))

# Sign the JWT
jwt_token = jwt_instance.encode(payload, private_key_jwk, 'RS256')

# Request an installation access token
headers = {
    'Authorization': f'Bearer {jwt_token}',
    'Accept': 'application/vnd.github+json',
}
url = f'https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens'

response = requests.post(url, headers=headers)
response.raise_for_status()  # Raise an error if the request failed

# Extract the token from the response
installation_access_token = response.json().get('token')

print("Installation Access Token:", installation_access_token)