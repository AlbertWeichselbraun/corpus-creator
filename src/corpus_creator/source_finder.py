#!/usr/bin/env python
# encoding: utf-8

'''
source finder
=============
uses a search engine to query for potential source documents (which is required
to use the corpus-creator with existing corpora

workflow
--------

1. obtain random snippets from the input text 
   (from "n" sentences with comprising an m-gram)
2. query a search engine for these snippets

.. codeauthor:: Albert Weichselbraun <albert@weichselbraun.net>
'''

from random import choice
from random import randint

from eWRT.ws.bing.search import BingSearch

class SourceFinder(object):

    def __init__(self, text, query_sentence_count=3, 
        query_n_gram_size=3):
        '''
        :param text: \
            the text for which we search the source file
        :param query_sentence_count: \
            maximum number of sentences to consider for the search
            engine query.
        :param query_n_gram_size: \
            number of coherent words to consider in the query
        '''
        self.query_string = get_query(text, query_sentence_count, query_n_gram_size)

    def search(self, search_engine, no_results):
        '''
        use the given search_engine to obtain potential sources
        :param search_engine: \
            an ``eWRT.ws.AbstractIterableWebSource`` used for the query.
        :param no_results: \
            the number of results to return.

        :returns: \
            a list of links with potential web sources
        '''
        results = search_engine.search_documents(self.query_string, no_results)
        results = results[:no_results]

        return [result['url'] for result in results]

    @staticmethod
    def get_query(text, query_sentence_count, query_n_gram_size):
        '''
        :returns: \
            the query for the given parameters
        '''
        query_string = [ '"{0}"'.format(SourceFinder.select_query_ngram(sentence))
                         for sentence in SourceFinder.select_query_sentences(
                         text, query_sentence_count)]
        return " ".join(query_string)

    @staticmethod
    def select_query_sentences(text, query_sentence_count):
        '''
        selects ``query_sentence_count`` sentences from the given text for the
        search engine query
        '''
        source_sentences = text.split("\n")
        query_sentence_count = min(len(source_sentences), query_sentence_count)

        query_sentences = set()
        while len(query_sentences) < query_sentence_count:
            query_sentences.add(choice(source_sentences))

        return query_sentences
    
    @staticmethod
    def select_query_ngram(sentence, query_n_gram_size):
        '''
        selects an n_gram of size ``query_n_gram_size`` from a sentence.

        :param sentences: \
            the sentence from which to selecte the n-gram
        :param query_n_gram_size: \
            the number of words to include in the result
        :returns: \
            a query string comprising ``query_n_gram_size`` words.
        '''
        words = sentence.split(" ")
        max_word_index = max(len(words)-query_n_gram_size, 0)

        word_index = randint(0, max_word_index)
        selected_words = words[word_index:word_index+query_n_gram_size]
        return " ".join(selected_words)

# ---------------------------------------------------------------------------
# Unittesting
# ---------------------------------------------------------------------------

def test_select_query_ngram():
    sentence = "hallo wie geht's"
    select = SourceFinder.select_query_ngram 
    assert select(sentence, 3) == "hallo wie geht's"
    assert select(sentence, 2) in ("hallo wie", "wie geht's")

    # test whether all correct solutions are found
    sentence = "Ana und Tom gehen spazieren."
    correct_solutions = ['Ana und Tom', 'und Tom gehen', 'Tom gehen spazieren.']
    found_solutions = set()
    while len(found_solutions) < len(correct_solutions):
        solution = select(sentence, 3)
        assert solution in correct_solutions
        found_solutions.add(solution)
