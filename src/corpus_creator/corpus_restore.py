#!/usr/bin/env python
# encoding: utf-8

''' 
corpus-restore
==============
Restores the text file based on the cdiff

.. codeauthor: Albert Weichselbraun <albert@weichselbraun.net>
'''

from os.path import join as os_join

from corpus_creator import checksum, get_text
from corpus_creator.cdiff_file import CDiffFile
from corpus_creator.corpus_diff import corpus_diff
from corpus_creator.toolkit import find_all, get_resource


def extract_sentence_from_trigram(from_text, sentence_len, start_trigram,
        end_trigram, sentence_hash):
    '''
    Extracts the given sentence based on the trigrams and len
    :param from_text: \
        the text from which the sentence is computed
    :param sentence_len: \
        the sentence's length
    :param start_trigram: \
        the trigram with which the sentence starts
    :param end_trigram: \
        the end trigram of the sentence
    :param sentence_hash: \
        the sentence's hash as computed with :func:`corpus_creator.checksum`

    :returns:
        sentence, checksum_correct
    '''
    trigram_start_positions = list(find_all(from_text, start_trigram))
    trigram_end_positions = list(find_all(from_text, end_trigram))

    valid_spawns = []

    for start_pos in trigram_start_positions:
        for end_pos in trigram_end_positions:
            if end_pos - start_pos + 3 == sentence_len:
                valid_spawns.append(start_pos)

    sentence = None
    for valid_spawn in valid_spawns:
        sentence = from_text[valid_spawn:valid_spawn+sentence_len]
        if checksum(sentence) == sentence_hash:
            return sentence, True

    return sentence, False


def extract_sentence(from_text, sentence_cdiff):
    '''
    :param from_text: \
        source text from which to extract relevant sentences.
    :param sentence_cdiff: \
        the cdiff used to extract the sentence.
    :returns: \
        sentence, if a valid sentence has been found (or None otherwise)
    '''
    sentence, is_valid = extract_sentence_from_trigram(
        from_text=from_text,
        sentence_len=sentence_cdiff.sentence_length, 
        start_trigram=sentence_cdiff.start_trigram, 
        end_trigram=sentence_cdiff.end_trigram, 
        sentence_hash=sentence_cdiff.sentence_hash)

    if is_valid:
        return sentence

    return None


def corpus_restore(diff_file, working_directory="", html_url=""):
    '''
    creates the corpus diff file for the given two texts.

    ::param diff_file:
        the diff_file
    ::param working_directory:
        an optional working_directory containing the HTML files.
    ::param html_url:
        optionally overwrite the url used in the diff_file (useful for testing)

    ::returns
        the text file used to create the cdiff
    '''
    cdiff = CDiffFile(diff_file)
    if html_url:
        fpath = os_join(working_directory, html_url)
    else:
        fpath = os_join(working_directory, cdiff.url)
    from_text = get_text(get_resource(fpath))

    sentences = filter(None, (extract_sentence(from_text, sentence_cdiff) 
                              for sentence_cdiff in cdiff.sentences))
    return "\n".join(sentences)


if __name__ == '__main__':
    TEXT = get_text(open("tests/Chur.html").read().decode("utf8"))
    #open("info.txt", "w").write(text.encode("utf8"))
    print corpus_diff(source_url='tests/Chur.html',
                      from_text=TEXT, 
                      to_text=open("tests/Chur.txt").read().decode("utf8").strip())
