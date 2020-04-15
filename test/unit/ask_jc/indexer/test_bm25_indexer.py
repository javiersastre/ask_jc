import io
import os

from ask_jc.indexer.bm25_indexer import Bm25Indexer

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'ask_jc', 'indexer')


def test_index_dataframe_and_save():
    expected_path = os.path.join(data_dir, 'bm25_index.pkl')
    with open(expected_path, 'rb') as fp:
        expected = fp.read()
    dataframe_pathname = os.path.join(data_dir, '..', 'paper', 'dataframe.gzip')
    indexer = Bm25Indexer()
    indexer.index_dataframe(dataframe_pathname)
    actual_file = io.BytesIO()
#    indexer.save_index(expected_path)
    indexer.save_index(actual_file)
    actual = actual_file.getvalue()
    assert actual == expected
