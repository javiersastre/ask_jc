import re

from ask_jc.normalizer.abstract_normalizer import AbstractNormalizer


class SpaceNormalizer(AbstractNormalizer):
    regex_expression = r'\s+'

    def __init__(self):
        self.pattern = re.compile(self.regex_expression)

    def normalize(self, text: str) -> str:
        normalized_text = self.pattern.sub(' ', text.strip())
        return normalized_text
