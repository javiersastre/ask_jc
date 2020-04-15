import argparse
import os
import sys

from ask_jc.indexer.bm25_indexer import Bm25Indexer
from ask_jc.paper.paper_sentence_dataframe import PaperSentenceDataFrame


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Converts all the paper sentences in a folder tree into a single'
                                                 ' dataframe pickle')
    parser.add_argument('--input', '-i', action='store', required=True, help="Path to folder with papers to convert")
    parser.add_argument('--output', '-o', action='store', required=True,
                        help="Path to output pkl file file where to save the dataframe; in case compression is to be"
                             "used, specify a compression file extension (e.g. gzip, bz2, zip or xz)")

    args = parser.parse_args()
    if not os.path.exists(args.input):
        print("Paper folder \"{}\" does not exist".format(args.input))
        sys.exit(1)
    return args


def main():
    args = parse_args()

    df = PaperSentenceDataFrame()
    df.load_folder(args.input)
    df.save_pickle(args.output)


if __name__ == '__main__':
    main()
