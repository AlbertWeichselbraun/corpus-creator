#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
from sys import stdout

from corpus_creator.corpus_restore import corpus_restore

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("input", help="The input file.")
    parser.add_argument("--output", "-o", help="An optional output file (default: stdout)", default=None)
    parser.add_argument("--working-directory", help="An optional working directory for on disk files", default="")
    parser.add_argument("--url", help="An optional url which overrides the url specified in the cdiff file", default=None)
    return parser.parse_args()


# -----------------------------------------------------------------
# main program
# -----------------------------------------------------------------
args = parse_arguments()
output_file = stdout if not args.output else open(args.output, 'w')

if args.input.endswith("cdiff"):
    sentences = corpus_restore(diff_file=args.input,
        working_directory=args.working_directory,
        html_url=args.url)

    output_file.write(sentences.encode("utf-8"))

