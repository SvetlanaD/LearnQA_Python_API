# homework for the Software-testing learning course Ex4

import requests

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)