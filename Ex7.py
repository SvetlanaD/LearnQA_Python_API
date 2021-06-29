import requests

address = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1 No required parameter "method" provided
response = requests.get(url=address)
print(response.text)
print(response.status_code)

# 2 HTTP method that is not supported by the backend is used in request
response = requests.patch(url=address)
print(response.text)
print(response.status_code)

# 3 Correct HTTP method and parameter "method"
response = requests.post(url=address,data={"method": "POST"})
print(response.text)
print(response.status_code)

# 4 Checking if the response doesn't comply with request
method_list = ["GET", "PUT", "POST", "DELETE"]
functions_list = ["get","put", "post", "delete"]

for method in method_list:
    for function_name in functions_list:
        function = getattr(requests, function_name)
        if function_name == "get":
            response = function(url=address, params={"method": method})
        else:
            response = function(url=address, data={"method": method})
        request_method = response.request.method
        response_text = response.text
        is_success = (response_text.find("success") != -1)

        if(request_method != method) and is_success:
            print(f'The response text is {response_text} if request method is {request_method} and parameter "method" equals {method}')
        if (request_method == method) and is_success is not True:
            print(f'The response text is {response_text} if request method is {request_method} and parameter "method" equals {method}')





