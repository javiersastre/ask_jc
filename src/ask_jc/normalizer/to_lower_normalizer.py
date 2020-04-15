from ask_jc.normalizer.abstract_normalizer import AbstractNormalizer


class ToLowerNormalizer(AbstractNormalizer):
    def normalize(self, text: str) -> str:
        return text.lower()
