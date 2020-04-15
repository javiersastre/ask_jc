import argparse
import os
import sys

from ask_jc.paper.paper_sentence_extractor import PaperSentenceExtractor


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Extract paper sentences')
    parser.add_argument('--input', '-i', action='store', required=True,
                        help="Path to paper file or folder in JSON format")
    parser.add_argument('--output', '-o', action='store', required=True,
                        help="Path to output file or folder; both input and output must either be files or folders; "
                             "in case they are folders, all JSON files in the input folder will be processed and the "
                             "sentences saved in a file per paper in the output folder")

    args = parser.parse_args()
    if not os.path.exists(args.input):
        print("Input file or folder \"{}\" does not exist".format(args.input))
        sys.exit(1)
    if os.path.isdir(args.input):
        if os.path.exists(args.output) and not os.path.isdir(args.output):
            print("Input is a folder but output is a file")
            sys.exit(1)
    else:
        if os.path.exists(args.output) and os.path.isdir(args.output):
            print("Input is a file but output is a folder")
            sys.exit(1)
    return args


def main():
    args = parse_args()

    extractor = PaperSentenceExtractor()
    extractor.extract_and_save(args.input, args.output)


if __name__ == '__main__':
    main()
