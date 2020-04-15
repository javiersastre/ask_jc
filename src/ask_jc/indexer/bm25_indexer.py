import datetime
import pickle
import time
from typing import Union, Optional

from ask_jc.paper.paper_sentence_dataframe import PaperSentenceDataFrame
from rank_bm25 import BM25Okapi
from tqdm.auto import tqdm
from typing.io import BinaryIO

from ask_jc.normalizer.to_lower_normalizer import ToLowerNormalizer
from ask_jc.tokenizer.simple_regex_tokenizer import SimpleRegexTokenizer


class Bm25Indexer(object):
    def __init__(self):
        self.tokenizer = SimpleRegexTokenizer()
        self.normalizer = ToLowerNormalizer()
        self.corpus = None
        self.index: Optional[BM25Okapi] = None

    def index_dataframe(self, dataframe_pathname: str):
        dataframe = PaperSentenceDataFrame()
        dataframe.load_pickle(dataframe_pathname)
        self.corpus = dataframe.corpus
        print('Tokenizing sentences')
        sentence_count = len(self.corpus.index)
        start_time = time.time()
        tokenized_corpus = [self.tokenizer.tokenize(self.normalizer.normalize(row['sentence']))
                            for i, row in tqdm(self.corpus.iterrows(), total=sentence_count)]
        elapsed_time = time.time() - start_time
        print('Sentences tokenized; elapsed time: {}'.format(str(datetime.timedelta(seconds=elapsed_time))))
        print('Building index')
        start_time = time.time()
        self.index = BM25Okapi(tokenized_corpus)
        elapsed_time = time.time() - start_time
        print('Index build completed; elapsed time: {}'.format(str(datetime.timedelta(seconds=elapsed_time))))

    def _save_index(self, file: BinaryIO):
        start_time = time.time()
        max_bytes = 2**31-1
        print('Serializing index')
        bytes = pickle.dumps(self.index)
        elapsed_time = time.time() - start_time
        print('Index serialized; elapsed time: {}'.format(str(datetime.timedelta(seconds=elapsed_time))))
        start_time = time.time()
        print('Writing index')
        for i in tqdm(range(0, len(bytes), max_bytes)):
            file.write(bytes[i:i + max_bytes])
            file.flush()
        elapsed_time = time.time() - start_time
        print('Index saved; elapsed time: {}'.format(str(datetime.timedelta(seconds=elapsed_time))))

    def save_index(self, pathname_or_file: Union[str, BinaryIO]):
        if isinstance(pathname_or_file, str):
            with open(pathname_or_file, 'wb') as fp:
                self._save_index(fp)
        else:
            self._save_index(pathname_or_file)
