import json
import os
import pathlib
from collections import OrderedDict
from typing import TextIO, List

import en_core_web_sm

from ask_jc.normalizer.space_normalizer import SpaceNormalizer


class PaperSentenceExtractor(object):
    def __init__(self):
        self.nlp = en_core_web_sm.load()
        self.space_normalizer = SpaceNormalizer()

    def extract_from_paragraph(self, paragraph: str) -> List[str]:
        doc = self.nlp(paragraph)
        sentences = [self.space_normalizer.normalize(sent.text) for sent in doc.sents]
        return sentences

    def extract_from_file(self, input: TextIO) -> OrderedDict:
        sentences = OrderedDict()
        paper = json.load(input, encoding='UTF-8')
        sentences['title'] = [self.extract_from_paragraph(paper['metadata']['title'])]
        sentences['abstract'] = [self.extract_from_paragraph(paragraph['text']) for paragraph in paper['abstract']]
        body_text = paper.get('body_text', [])
        sentences['body'] = [self.extract_from_paragraph(paragraph['text']) for paragraph in body_text]
        return sentences

    def extract_from_file_and_save_to_file(self, input: TextIO, output: TextIO):
        sentences = self.extract_from_file(input)
        json.dump(sentences, output, ensure_ascii=False, indent=4)

    def extract_from_folder_and_save_to_folder(self, input_pathname: str, output_pathname: str):
        pathlib.Path(output_pathname).mkdir(parents=True, exist_ok=True)
        for filename in sorted(os.listdir(input_pathname)):
            if filename.lower().endswith(".json"):
                in_file_pathname = os.path.join(input_pathname, filename)
                out_file_pathname = os.path.join(output_pathname, os.path.splitext(filename)[0] + '.json')
                print('Processing file {}'.format(in_file_pathname))
                with open(in_file_pathname, 'rt', encoding='UTF-8') as input:
                    with open(out_file_pathname, 'wt', encoding='UTF-8') as output:
                        self.extract_from_file_and_save_to_file(input, output)

    def extract_and_save(self, input_pathname, output_pathname):
        if os.path.isfile(input_pathname):
            with open(input_pathname, 'rt', encoding='UTF-8') as input:
                with open(output_pathname, 'wt', encoding='UTF-8') as output:
                    self.extract_from_file_and_save_to_file(input, output)
        else:
            self.extract_from_folder_and_save_to_folder(input_pathname, output_pathname)
