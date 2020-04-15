import argparse
import os
import sys

from ask_jc.indexer.bm25_indexer import Bm25Indexer


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Builds a BM25 index for the given dataframe pickle file')
    parser.add_argument('--input', '-i', action='store', required=True, help="Path to dataframe pickle file")
    parser.add_argument('--output', '-o', action='store', required=True, help="Path to output file")

    args = parser.parse_args()
    if not os.path.exists(args.input):
        print("Dataframe file \"{}\" does not exist".format(args.input))
        sys.exit(1)
    return args


def main():
    args = parse_args()

    indexer = Bm25Indexer()
    indexer.index_dataframe(args.input)
    indexer.save_index(args.output)


if __name__ == '__main__':
    main()
