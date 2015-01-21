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

        with open(fname) as f:
            self.url = f.next()

            # read sentence information
            for line in f:
                if line.startswith(">"):
                    self.sentences.append(self._parse_sentence_diff(line))

    @classmethod
    def _parse_sentence_diff(cls, line):
        start_trigram, end_trigram, sentence_length, sentence_hash = line.strip().split(" ")[1:]
        return CDiff(start_trigram,
                     end_trigram,
                     int(sentence_length),
                     sentence_hash)


def test_parse_sentence_diff():
    sentence_diff_line = '> Chu on. 110 cc269d'
    cdiff = CDiffFile._parse_sentence_diff(sentence_diff_line)

    assert cdiff == CDiff(start_trigram='Chu',
                          end_trigram='on.',
                          sentence_length='110',
                          sentence_hash='cc269d')


