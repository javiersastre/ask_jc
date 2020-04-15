import datetime
import os
import pickle
import time
from typing import List, Optional

import numpy as np
import pandas as pd

from ask_jc.paper.paper_sentence_dataframe import PaperSentenceDataFrame
from tqdm.auto import tqdm

from ask_jc.normalizer.to_lower_normalizer import ToLowerNormalizer
from ask_jc.tokenizer.simple_regex_tokenizer import SimpleRegexTokenizer
from ask_jc.util.bisect import bisect_left_with_key


class Bm25Searcher(object):
    HITS_COLUMNS = PaperSentenceDataFrame.COLUMNS.copy()
    HITS_COLUMNS.insert(0, 'score')

    def __init__(self):
        self.tokenizer = SimpleRegexTokenizer()
        self.normalizer = ToLowerNormalizer()
        self.dataset_names: Optional[List[str]] = None
        self.corpus = None
        self.index = None

    def load_sentences_and_index(self, sentences_pathname: str, index_pathname: str):
        print("Loading corpus")
        df = PaperSentenceDataFrame()
        df.load_pickle(sentences_pathname)
        self.corpus = df.corpus
        print("Loading index")
        start_time = time.time()
        max_bytes = 2**31-1
        bytes = bytearray(0)
        input_size = os.path.getsize(index_pathname)
        with open(index_pathname, 'rb') as fp:
            for _ in tqdm(range(0, input_size, max_bytes)):
                bytes += fp.read(max_bytes)
        self.index = pickle.loads(bytes)
        elapsed_time = time.time() - start_time
        print('Index loaded; elapsed time: {}'.format(str(datetime.timedelta(seconds=elapsed_time))))

    def search(self, query: str, max_docs=0, threshold=0.) -> pd.DataFrame:
        start_time = time.time()
        tokenized_query = self.tokenizer.tokenize(self.normalizer.normalize(query))
        scores = self.index.get_scores(tokenized_query)
        sorted_documents_by_score = np.argsort(scores)
        i = bisect_left_with_key(sorted_documents_by_score, threshold, lambda s: scores[s])
        if max_docs > 0:
            i = len(self.corpus) - min(len(self.corpus) - i, max_docs)
        selected_sorted_documents = list(reversed(sorted_documents_by_score[i:]))
        selected_sorted_scores = [scores[i] for i in selected_sorted_documents]
        hits = self.corpus.iloc[selected_sorted_documents].copy()
        hits['score'] = selected_sorted_scores
        hits = hits.reindex(columns=self.HITS_COLUMNS)
        elapsed_time = time.time() - start_time
        print('Found {} docs; elapsed time: {}'.format(len(hits), str(datetime.timedelta(seconds=elapsed_time))))
        return hits
