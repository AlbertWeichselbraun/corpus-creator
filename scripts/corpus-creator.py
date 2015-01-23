#!/usr/bin/env python3
# encoding: utf-8

from argparse import ArgumentParser
from sys import stdout

from corpus_creator.corpus_restore import corpus_restore
from corpus_creator.corpus_diff import get_diff
from corpus_creator.source_finder import SourceFinder
from corpus_creator.toolkit import get_resource

from eWRT.ws.bing.search import BingSearch

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("cdiff", help="The cdiff file to read or write.")
    parser.add_argument("--html-resource", help="URL of the HTML resource", default=None)
    parser.add_argument("--bing-api-key", help="Search for the source files on bing using the given api key")
    parser.add_argument("--bing-api-user", help="Search for the source files on bing using the given bing user")
    parser.add_argument("--search-appendix", nargs="+", default=[], help="Optinal additional search parameters")
    parser.add_argument("--txt-resource", help="URL of the input text resource", default=None)
    parser.add_argument("--output", "-o", help="An optional output file (default: stdout)", default=None)
    parser.add_argument("--working-directory", help="An optional working directory for on disk files", default="")
    parser.add_argument("--url", help="An optional url which overrides the url specified in the cdiff file", default=None)
    return parser.parse_args()


# -----------------------------------------------------------------
# main program
# -----------------------------------------------------------------
args = parse_arguments()
output_file = stdout if not args.output else open(args.output, 'w')

if args.txt_resource:
    if not args.html_resource and (args.bing_api_key and args.bing_api_user):
        print("Warning: No source file specified. Trying to query bing for potential matches.")
        search_engine = BingSearch(args.bing_api_key, args.bing_api_user)
        text = get_resource(args.txt_resource)
        source_finder = SourceFinder(text=text)
        results = source_finder.search(search_engine=search_engine, 
            search_suffix=args.search_appendix, no_results=5)
        source_url = results[0]
        print("Source url: {0}".format(source_url))
    else:
        source_url = args.html_resource
    with open(args.cdiff, 'w') as f:
        f.write(get_diff(destination_url=args.txt_resource, source_url=source_url))
else:
    # apply cdiff
    sentences = corpus_restore(diff_file=args.cdiff,
        working_directory=args.working_directory,
        html_url=args.url)

    output_file.write(sentences)
