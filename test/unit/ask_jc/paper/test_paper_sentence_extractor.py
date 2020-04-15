import os
from io import StringIO

import pytest

from ask_jc.paper.paper_sentence_extractor import PaperSentenceExtractor

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'ask_jc', 'paper')


@pytest.fixture
def paper_sentence_extractor1() -> PaperSentenceExtractor:
    extractor = PaperSentenceExtractor()
    yield extractor


extract_test_cases = [
    ('biorxiv_medrxiv', '0a27cb2cd52229472fcfc3e49d3a3cb7179867e4.json'),
    ('comm_use_subset', '0a00a6df208e068e7aa369fb94641434ea0e6070.json')
]


@pytest.mark.parametrize("paper_folder, paper_file", extract_test_cases)
def test_extract(paper_folder, paper_file, paper_sentence_extractor1):
    input_pathname = os.path.join(data_dir, 'original', paper_folder, paper_file)
    expected_pathname = os.path.join(data_dir, 'sentences', paper_folder, paper_file)
    with open(expected_pathname, 'rt', encoding='UTF-8') as fp:
        expected = fp.read()
    with open(input_pathname, 'rt', encoding='UTF-8') as input:
        output = StringIO()
        paper_sentence_extractor1.extract_from_file_and_save_to_file(input, output)
        actual = output.getvalue()
        output.close()
    assert actual == expected
