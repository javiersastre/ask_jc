from ask_jc.tokenizer.regex_tokenizer import RegexTokenizer


class SimpleRegexTokenizer(RegexTokenizer):
    __regex_exp = r"['\w\d-]+|\S"

    def __init__(self):
        super().__init__(self.__regex_exp)
