import os
from io import StringIO

from ask_jc.paper.paper_sentence_dataframe import PaperSentenceDataFrame


data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'ask_jc', 'paper')
temp_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'temp')

if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)


def test_load_from_folder_and_save_to_csv():
    input_pathname = os.path.join(data_dir, 'sentences')
    expected_pathname = os.path.join(data_dir, 'dataframe.csv')
    with open(expected_pathname, 'rt', encoding='UTF-8') as fp:
        expected = fp.read()
    df = PaperSentenceDataFrame()
    df.load_folder(input_pathname)
    output = StringIO()
    df.save_csv(output)
    actual = output.getvalue()
    assert actual == expected


def test_load_csv_and_save_csv():
    expected_pathname = os.path.join(data_dir, 'dataframe.csv')
    with open(expected_pathname, 'rt', encoding='UTF-8') as fp:
        expected = fp.read()
    df = PaperSentenceDataFrame()
    df.load_csv(expected_pathname)
    output = StringIO()
    df.save_csv(output)
    actual = output.getvalue()
    assert actual == expected


def test_read_csv_save_pickle_load_pickle_save_csv():
    expected_pathname = os.path.join(data_dir, 'dataframe.csv')
    with open(expected_pathname, 'rt', encoding='UTF-8') as fp:
        expected = fp.read()
    pickle_pathname = os.path.join(temp_dir, 'dataframe.gzip')
    if os.path.exists(pickle_pathname):
        os.remove(pickle_pathname)
    df = PaperSentenceDataFrame()
    df.load_csv(expected_pathname)
    df.save_pickle(pickle_pathname)

    df = PaperSentenceDataFrame()
    df.load_pickle(pickle_pathname)
    output = StringIO()
    df.save_csv(output)
    actual = output.getvalue()
    assert actual == expected
