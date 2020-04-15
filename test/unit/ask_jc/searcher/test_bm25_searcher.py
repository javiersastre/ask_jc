import io
import os

import pytest

from ask_jc.searcher.bm25_searcher import Bm25Searcher


data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'ask_jc', 'searcher')


@pytest.fixture
def bm25_searcher1() -> Bm25Searcher:
    sentences_path = os.path.join(data_dir, '..', 'paper', 'dataframe.gzip')
    index_path = os.path.join(data_dir, '..', 'indexer', 'bm25_index.pkl')
    searcher = Bm25Searcher()
    searcher.load_sentences_and_index(sentences_path, index_path)
    yield searcher


search_test_cases = [
    ('BCG vaccine', 100, 1.),
    ('BCG vaccine', 2, 1.)
]


@pytest.mark.parametrize("query, max_docs, threshold", search_test_cases)
def test_search(query: str, max_docs: int, threshold: float, bm25_searcher1: Bm25Searcher):
    expected_path = os.path.join(data_dir, query.replace(' ', '-') + '_' + str(max_docs) + '_' + str(threshold) +
                                 '.csv')
    with open(expected_path, 'rt', encoding='UTF-8') as fp:
        expected = fp.read()
    hits = bm25_searcher1.search('BCG vaccine', max_docs, threshold)
    actual_file = io.StringIO()
    hits.to_csv(actual_file, float_format='%.2f', index=False)
    actual = actual_file.getvalue()
    assert actual == expected
