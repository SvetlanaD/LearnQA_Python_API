class TestEx10:
    @staticmethod
    def test_check_phrase():
        phrase = input("Set a phrase shorter than 15 symbols: ")
        phrase_length = len(phrase)
        assert phrase_length < 15, f"The number of symbols = {phrase_length} is longer or equal to 15"


