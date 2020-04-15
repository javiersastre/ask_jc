from enum import Enum


class BlockId(Enum):
    TITLE = 0
    ABSTRACT = 1
    BODY = 2


class SentenceId(object):
    def __init__(self, dataset_id: int, paper_id: int, block_id: int, section_number: int, sentence_number: int):
        self.dataset_id = dataset_id
        self.paper_id = paper_id
        self.block_id = block_id
        self.section_number = section_number
        self.sentence_number = sentence_number

    def _paper_id_to_str(self) -> str:
        s = hex(self.paper_id).lstrip('0x')
        while len(s) < 40:
            s = '0' + s
        return s

    def __str__(self):
        return str(self.dataset_id) + '\t' + self._paper_id_to_str() + '\t' + str(self.block_id) + '\t' +\
               str(self.section_number) + '\t' + str(self.sentence_number)
