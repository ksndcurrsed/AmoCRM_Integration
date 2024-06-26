import requests
import json
from datetime import datetime

# Load configuration from config.py
from config import AMOINFO

link = f"https://{AMOINFO['subdomain']}.amocrm.ru/oauth2/access_token"

# Data for the request
data = {
    'client_id': AMOINFO['client_id'],
    'client_secret': AMOINFO['client_secret'],
    'grant_type': 'authorization_code',
    'code': AMOINFO['code'],
    'redirect_uri': 'https://google.com',
}

# HTTP request headers
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'amoCRM-oAuth-client/1.0',
}

# Making the request
response = requests.post(link, headers=headers, data=json.dumps(data))

# Handling response
code = response.status_code
errors = {
    400: 'Bad request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not found',
    500: 'Internal server error',
    502: 'Bad gateway',
    503: 'Service unavailable',
}

try:
    # If response code is not successful, raise an exception
    if code < 200 or code > 204:
        raise Exception(errors.get(code, 'Undefined error'), code)
except Exception as e:
    print(f'Ошибка: {e.args[0]}\nКод ошибки: {e.args[1]}')
    exit()

# Parsing JSON response
response_data = response.json()

# Calculating expiration time and formatting data
expiration_time = datetime.now().timestamp() + response_data['expires_in']
info = f"{expiration_time}x-amo-checker-info-amo;;;{response_data['access_token']}x-amo-checker-info-amo;;;{response_data['refresh_token']}"

# Writing data to file
with open("refresh.txt", "w") as file:
    file.write(info)

print("Всё окей!")
