import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
history_list = response.history
history_length = len(history_list)
final_address = history_list[history_length-1].headers["Location"]

print(f'Final address is {final_address}')
print(f'Number of redirects is {history_length}')
