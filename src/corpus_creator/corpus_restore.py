#!/usr/bin/env python
# encoding: utf-8

''' 
corpus-restore
restores the text file based on the cdiff

::author: Albert Weichselbraun <albert@weichselbraun.net>

TODO: more robust handling of changed files
'''

from collections import Counter, namedtuple
from random import choice
from string import ascii_letters
from os.path import join as os_join
from operator import attrgetter

from corpus_creator import checksum, get_text
from corpus_creator.cdiff_file import CDiffFile
from corpus_creator.toolkit import find_all, get_resource

ALPHANUMMERIC = ascii_letters + u"äöüÄÖÜßèéêÊÉçàô"

Anchor = namedtuple("Anchor", "name old_pos current_pos")

def determine_anchor_positions(from_text, anchors):
    '''
    ensures that the anchors are still valid (i.e. unique)
    and returns their positions within the HTML file
    '''
    valid_anchors = [Anchor(name=anchor, old_pos=pos, current_pos=from_text.find(anchor))
                     for pos, anchor in anchors.items() if from_text.count(anchor) == 1]
    return valid_anchors


def extract_sentence_from_index(from_text, anchors, sentence_cdiff):
    '''
    Extracts the given sentence and returns whether it has been an exact match

    ::returns
        sentence, checksum_correct
    '''
    sentence = None
    for anchor, relative_sentence_pos in zip(sorted(anchors, key=attrgetter('old_pos')), sentence_cdiff.positions):
        sentence_start_pos = anchor.current_pos + relative_sentence_pos
        sentence = from_text[sentence_start_pos:sentence_start_pos+sentence_cdiff.sentence_length]
        if checksum(sentence) == sentence_cdiff.sentence_hash:
            return sentence, True

    return sentence, False


def extract_sentence_from_trigram(from_text, sentence_len, start_trigram, end_trigram, sentence_hash):
    '''
    Extracts the given sentence based on the trigrams and len

    ::returns
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


def extract_sentence(from_text, anchors, sentence_cdiff):
    '''
    ::returns
        sentence, if a valid sentence has been found (or None otherwise)
    '''
    sentence, is_valid = extract_sentence_from_index(
        from_text=from_text, 
        anchors=anchors,
        sentence_cdiff=sentence_cdiff)

    if is_valid:
        return sentence

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
    # open("info.txt", "w").write(from_text.encode("utf-8"))
    anchors = determine_anchor_positions(from_text, cdiff.anchors)

    sentences = filter(None, (extract_sentence(from_text, anchors, sentence_cdiff) 
                              for sentence_cdiff in cdiff.sentences))
    return "\n".join(sentences)


if __name__ == '__main__':
    text = get_text(open("tests/Chur.html").read().decode("utf8"))
    #open("info.txt", "w").write(text.encode("utf8"))
    print corpus_diff(text, open("tests/Chur.txt").read().decode("utf8").strip())
