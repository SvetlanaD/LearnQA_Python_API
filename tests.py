# homework for the Software-testing learning course Ex4

import requests

payload = {"name": "Svetlana Den"}
response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
print(response.text)