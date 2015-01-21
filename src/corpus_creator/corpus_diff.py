#!/usr/bin/env python
# encoding: utf-8

'''
corpus-diff
computes the corpus diff

.. codeauthor:: Albert Weichselbraun <albert@weichselbraun.net>
'''
from warnings import warn

from corpus_creator import checksum, get_text
from corpus_creator.toolkit import get_resource

def corpus_diff(source_url, from_text, to_text):
    '''
    creates the corpus diff file for the given two texts.
    '''
    diff = [source_url]

    for sentence in to_text.split("\n"):
        sentence = sentence.strip()
        if not sentence: 
            continue
        elif not sentence in from_text:
            warn("Skipping sentence: The source file does not contain the following sentence: '{sentence}'. Cdiff won't be able to recreate it.".format(
                sentence=sentence.encode("utf8")))
            continue
        sentence_diff = [">"]
        # add letters, len and checksum
        sentence_diff.append(sentence[:3].encode("utf8"))
        sentence_diff.append(sentence[-3:].encode("utf8"))
        sentence_diff.append(str(len(sentence)))
        sentence_diff.append(checksum(sentence))

        # add diff
        diff.append(" ".join(sentence_diff))

    return "\n".join(diff)


def get_diff(destination_url, source_url):
    '''
    helper function to compute the cdiff based on the text file
    in destination_url and the source specified in source_url.

    :param destination_url: \
        destination file with the corpus text to extract
    :param source_url: \
        the (html) source file from which the corpus text
        is extracted
    :returns: \
        the cdiff required to extract the destination text from the
        input specified in the source_url.
    '''
    from_text = get_text(get_resource(source_url))
    to_text = get_resource(destination_url)
    return corpus_diff(source_url, from_text, to_text)
