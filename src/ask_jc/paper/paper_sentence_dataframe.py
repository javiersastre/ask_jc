import datetime
import json
import os
import time
from typing import List, Union, Set, TextIO

import numpy as np
import pandas as pd

from ask_jc.paper.sentence_id import BlockId


class PaperSentenceDataFrame(object):
    COLUMNS = [
            'dataset_id',
            'paper_id',
            'block_id',
            'section_number',
            'sentence_number',
            'sentence'
    ]
    DTYPES = {
        'dataset_id': np.object,
        'paper_id': np.object,
        'block_id': np.int64,
        'section_number': np.int64,
        'sentence_number': np.int64,
        'sentence': np.object
    }

    def __init__(self):
        self.corpus = None

    def append_section_rows(self, section_rows: List[List], dataset_id: str, paper_id: str, block_id: int,
                            sections: List[List[str]]):
        section_number = 0
        for section in sections:
            sentence_number = 0
            for sentence in section:
                section_rows.append([dataset_id, paper_id, block_id, section_number, sentence_number, sentence])
                sentence_number += 1
            section_number += 1

    def _load_folder(self, section_rows: List[List], folder_pathname: str, dataset_id: str):
        for filename in sorted(os.listdir(folder_pathname)):
            pathname = os.path.join(folder_pathname, filename)
            if os.path.isfile(pathname) and filename.lower().endswith(".json"):
                print('Loading file {}'.format(pathname))
                paper_id = os.path.splitext(filename)[0]
                # paper_id = int(os.path.splitext(filename)[0], 16)
                with open(pathname, 'rt', encoding='UTF-8') as input:
                    sentences = json.load(input)
                    self.append_section_rows(section_rows, dataset_id, paper_id, BlockId.TITLE.value,
                                             sentences['title'])
                    self.append_section_rows(section_rows, dataset_id, paper_id, BlockId.ABSTRACT.value,
                                             sentences['abstract'])
                    self.append_section_rows(section_rows, dataset_id, paper_id, BlockId.BODY.value,
                                             sentences['body'])

    def add_dataset_folders(self, folder_pathname: str, dataset_folders: Set):
        for filename in os.listdir(folder_pathname):
            file_or_folder_pathname = os.path.join(folder_pathname, filename)
            if os.path.isdir(file_or_folder_pathname):
                self.add_dataset_folders(file_or_folder_pathname, dataset_folders)
            elif filename.lower().endswith(".json"):
                dataset_folders.add(folder_pathname)

    def get_dataset_folders(self, folder_pathname: str) -> List:
        dataset_folders = set()
        self.add_dataset_folders(folder_pathname, dataset_folders)
        return list(sorted(dataset_folders))

    def load_folder(self, folder_pathname: str):
        print('Loading sentences')
        start_time = time.time()
        if folder_pathname.endswith('/') or folder_pathname.endswith('\\'):
            folder_pathname = folder_pathname[:-1]
        dataset_folders = self.get_dataset_folders(folder_pathname)
        dataset_names = [dataset_folder[len(folder_pathname) + 1:] for dataset_folder in dataset_folders]
        section_rows = []
        for dataset_name, dataset_folder in zip(dataset_names, dataset_folders):
            self._load_folder(section_rows, dataset_folder, dataset_name)
        self.corpus = pd.DataFrame(section_rows, columns=self.COLUMNS)
        elapsed_time = time.time() - start_time
        print('Sentences loaded; elapsed time: {}'.format(str(datetime.timedelta(seconds=elapsed_time))))

    def load_pickle(self, pathname: str):
        print('Loading pickle')
        start_time = time.time()
        self.corpus = pd.read_pickle(pathname)
        elapsed_time = time.time() - start_time
        print('Pickle loaded; elapsed time: {}'.format(str(datetime.timedelta(seconds=elapsed_time))))

    def save_pickle(self, pathname: str):
        print('Saving pickle')
        start_time = time.time()
        self.corpus.to_pickle(pathname)
        elapsed_time = time.time() - start_time
        print('Pickle saved; elapsed time: {}'.format(str(datetime.timedelta(seconds=elapsed_time))))

    def load_csv(self, pathname_or_file: Union[str, TextIO]):
        print('Loading CSV')
        start_time = time.time()
        self.corpus = pd.read_csv(pathname_or_file, dtype=self.DTYPES)
        elapsed_time = time.time() - start_time
        print('Pickle saved; elapsed time: {}'.format(str(datetime.timedelta(seconds=elapsed_time))))

    def save_csv(self, pathname_or_file: Union[str, TextIO]):
        print('Saving CSV')
        start_time = time.time()
        self.corpus.to_csv(pathname_or_file, index=False)
        elapsed_time = time.time() - start_time
        print('CSV saved; elapsed time: {}'.format(str(datetime.timedelta(seconds=elapsed_time))))
