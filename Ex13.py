import requests
import pytest


class TestEx13:
    agent0 = "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
    agent1 = "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1"
    agent2 = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    agent3 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0"
    agent4 = "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    response_exp = [({"user_agent": agent0,
                      "platform": "Mobile",
                      "browser": "No",
                      "device": "Android"}),
                    ({"user_agent": agent1,
                      "platform": "Mobile",
                      "browser": "Chrome",
                      "device": "iOS"}),
                    ({"user_agent": agent2,
                      "platform": "Googlebot",
                      "browser": "Unknown",
                      "device": "Unknown"}),
                    ({"user_agent": agent3,
                      "platform": "Web",
                      "browser": "Chrome",
                      "device": "No"}),
                    ({"user_agent": agent4,
                      "platform": "Mobile",
                      "browser": "No",
                      "device": "iPhone"})
                    ]

    @pytest.mark.parametrize("response_exp", response_exp)
    def test_user_agent(self, response_exp):
        user_agent = response_exp["user_agent"]
        response_act = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check",
                                    headers={"User-Agent": user_agent}).json()
        for header_exp in response_exp.keys():
            if header_exp != "user_agent":
                assert header_exp in response_act.keys(), f"Header {header_exp} is not in response json {response_act}"
                value_act = response_act[header_exp]
                value_exp = response_exp[header_exp]
                assert value_exp == value_act, f"User Agent: {user_agent}." \
                                               f" Actual header {header_exp} value {value_act} isn't equal to expected {value_exp}"
