import re
from typing import List


class RegexTokenizer:
    def __init__(self, regex_expression: str):
        self.pattern = re.compile(regex_expression, re.IGNORECASE)

    def tokenize(self, text: str) -> List[str]:
        return self.pattern.findall(text)
