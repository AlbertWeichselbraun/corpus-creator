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

class SourceFinder(object):

    def __init__(self, text, query_sentence_count=7, 
        query_n_gram_size=7):
        '''
        :param text: \
            the text for which we search the source file
        :param query_sentence_count: \
            maximum number of sentences to consider for the search
            engine query.
        :param query_n_gram_size: \
            number of coherent words to consider in the query
        '''
        self.search_terms = self.get_search_terms(text, query_sentence_count, 
                query_n_gram_size)

    def search(self, search_engine, search_suffix=[], no_results=1):
        '''
        use the given search_engine to obtain potential sources
        :param search_engine: \
            an ``eWRT.ws.AbstractIterableWebSource`` used for the query.
        :param search_suffix: \
            an optional list of additional search strings (e.g. ``['site:nzz.ch']``)
        :param no_results: \
            the number of results to return.

        :returns: \
            a list of links with potential web sources
        '''
        self.search_terms.extend(search_suffix)
        # print(self.search_terms)
        # print(" ".join(self.search_terms))
        results = list(search_engine.search_documents([" ".join(self.search_terms)], no_results))
        results = results[:no_results]

        return [result['url'] for result in results]

    @staticmethod
    def get_search_terms(text, query_sentence_count, query_n_gram_size):
        '''
        :returns: \
            a list of search terms obtained from the given text
        '''
        return [ SourceFinder.select_query_ngram(sentence, query_n_gram_size)
                 for sentence in SourceFinder.select_query_sentences(text, query_sentence_count)]

    @staticmethod
    def select_query_sentences(text, query_sentence_count):
        '''
        selects ``query_sentence_count`` sentences from the given text for the
        search engine query
        '''
        source_sentences = [sentence.strip() 
                            for sentence in text.strip().split("\n") 
                            if sentence.strip()]
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
        selected_alnum_words = [word for word in selected_words if word.isalnum()]
        
        # only quote the string if all words are alphanumerical
        search_words = " ".join(selected_alnum_words)
        if len(selected_words) == len(selected_alnum_words):
            return '"{0}"'.format(search_words)
        else:
            return search_words

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
