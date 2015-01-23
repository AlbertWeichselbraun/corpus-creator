#!/usr/bin/env python
# encoding: utf-8

'''
Encapsulates a cdiff file
'''

from collections import namedtuple

CDiff = namedtuple('CDiff', 'start_trigram end_trigram sentence_length sentence_hash')

class CDiffFile(object):
    
    def __init__(self, fname):
        self.sentences = []
        self.url = None

        with open(fname) as f:
            # read sentence information
            for line in f:
                if not self.url:
                    self.url = line.strip()
                elif line.startswith(">"):
                    self.sentences.append(self._parse_sentence_diff(line))

    @classmethod
    def _parse_sentence_diff(cls, line):
        start_trigram = line[2:5]
        end_trigram = line[6:9]
        sentence_length, sentence_hash = line[10:].strip().split(" ")
        return CDiff(start_trigram,
                     end_trigram,
                     int(sentence_length),
                     sentence_hash)


def test_parse_sentence_diff():
    sentence_diff_line = '> Chu on. 110 cc269d'
    cdiff = CDiffFile._parse_sentence_diff(sentence_diff_line)

    assert cdiff == CDiff(start_trigram='Chu',
                          end_trigram='on.',
                          sentence_length=110,
                          sentence_hash='cc269d')

    # test trigrams with spaces
    sentence_diff_line = '> A h  i. 110 cc269d'
    cdiff = CDiffFile._parse_sentence_diff(sentence_diff_line)

    assert cdiff == CDiff(start_trigram='A h',
                          end_trigram=' i.',
                          sentence_length=110,
                          sentence_hash='cc269d')



