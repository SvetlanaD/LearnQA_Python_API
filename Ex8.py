import requests
import time

address = "https://playground.learnqa.ru/ajax/api/longtime_job"
# creating job and getting token
response = requests.get(address)
wait_time = response.json()["seconds"]
token = response.json()["token"]
print(f'Token is: {token}')
payload = {"token": token}

# checking the response while the job isn't ready yet
response2 = requests.get(address, params=payload)
is_correct_response = (response2.json()["status"] == "Job is NOT ready")
if not is_correct_response:
    print(f"The response text isn't as expected: {response2.text} and status code is: {response2.status_code}")

# checking the response when the job is ready
time.sleep(wait_time)
response3 = requests.get(address, params=payload)
is_correct_response = (response3.json()["status"] == "Job is ready" and ("result" in response3.json().keys()))
if not is_correct_response:
    print(f"The correct response text isn't as expected: {response3.text} and status code is: {response3.status_code}")