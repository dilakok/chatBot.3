import requests
import json

headers = {
    'inp': "Hello"
}

response = requests.post(url='http://127.0.0.1:7201/info', json=headers)
print(response.json())
