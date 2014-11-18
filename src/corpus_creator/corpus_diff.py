#!/usr/bin/env python
# encoding: utf-8

''' corpus-diff
    computes the corpus diff
'''

from collections import Counter
from random import choice
from string import ascii_letters

from corpus_creator import checksum, get_text

ALPHANUMMERIC = ascii_letters + u"äöüÄÖÜßèéêÊÉçàô"

def suggest_anchors(from_text, num_anchors):
    '''
    ::param num_anchors: 
        suggests num_anchors based on the from_text

    Note: no colon ":" may occur in an anchor and it must start with
          a alphanumeric letter.
    '''
    assert num_anchors >= 2

    # determine word frequencies
    counter = Counter()
    counter.update(from_text.split())

    # determine anchor positions
    position_anchor_dict = {from_text.find(anchor): anchor 
                            for anchor in counter if counter[anchor] == 1 and len(anchor) > 2 and not ':' in anchor and anchor[0] in ALPHANUMMERIC} 

    # add the first and last anchor
    result_indices = set()
    result_indices.add(min(position_anchor_dict))
    result_indices.add(max(position_anchor_dict))
    
    while len(result_indices) < num_anchors and len(result_indices) < len(position_anchor_dict):
        result_indices.add(choice(position_anchor_dict.keys()))

    return {result_index: position_anchor_dict[result_index] 
            for result_index in result_indices}


def corpus_diff(from_text, to_text):
    '''
    creates the corpus diff file for the given two texts.
    '''
    diff = []
    anchors = suggest_anchors(from_text, num_anchors=7)
    # add anchors and positions
    diff.append(" ".join(["%s:%s" %(anchor.encode("utf8"),pos) 
                for pos,anchor in sorted(anchors.items())]))

    for sentence in to_text.split("\n"):
        sentence = sentence.strip()
        sentence_diff = [">"]
        start_index = from_text.find(sentence)     
        # add indices
        for anchor_index in anchors:
            sentence_diff.append(str(start_index-anchor_index))

        # add letters, len and checksum
        sentence_diff.append(sentence[:3].encode("utf8"))
        sentence_diff.append(sentence[-3:].encode("utf8"))
        sentence_diff.append(str(len(sentence)))
        sentence_diff.append(checksum(sentence))

        # add diff
        diff.append(" ".join(sentence_diff))

    return "\n".join(diff)


if __name__ == '__main__':
    text = get_text(open("tests/Chur.html").read().decode("utf8"))
    #open("info.txt", "w").write(text.encode("utf8"))
    print corpus_diff(text, open("tests/Chur.txt").read().decode("utf8").strip())
