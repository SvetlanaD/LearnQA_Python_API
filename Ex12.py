import requests


class TestEx12:
    @staticmethod
    def test_homework_header():
        exp_header = 'x-secret-homework-header'
        exp_value = 'Some secret value'
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        response_headers = response.headers.keys()
        assert exp_header in response_headers, f"Header {exp_header} isn't in the response headers"
        response_header_value = response.headers[exp_header]
        assert exp_value == response_header_value, \
            f"Header {exp_header} value: {response_header_value} isn't equal to expected {exp_value}"

