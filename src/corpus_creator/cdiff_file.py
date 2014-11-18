#!/usr/bin/env python
# encoding: utf-8

'''
Encapsulates a cdiff file
'''

from collections import namedtuple

CDiff = namedtuple('CDiff', 'positions start_trigram end_trigram sentence_length sentence_hash')

class CDiffFile(object):
    
    def __init__(self, fname):
        self.anchors = []
        self.sentences = []

        with open(fname) as f:
            self.url = f.next()
            self.anchors = self._parse_anchors(f.next())

            # read sentence information
            for line in f:
                if line.startswith(">"):
                    self.sentences.append(self._parse_sentence_diff(line))


    @classmethod
    def _parse_anchors(cls, line):
        anchors = {}
        for anchor_entry in line.strip().split():
            anchor, pos = anchor_entry.split(':')
            anchors[int(pos)] = anchor
        return anchors

    @classmethod
    def _parse_sentence_diff(cls, line):
        lst = line.strip().split(" ")[1:]
        return CDiff(positions=map(int, lst[:-4]),
                     start_trigram=lst[-4].decode("utf8"),
                     end_trigram=lst[-3].decode("utf8"),
                     sentence_length=int(lst[-2]),
                     sentence_hash=lst[-1])


def test_anchor_parsing():
    anchor_line = 'Wikipedia,:13 Terracina:1005 seat:2285 sites;:8589'
    anchors = CDiffFile._parse_anchors(anchor_line)

    assert anchors == {13: 'Wikipedia,', 1005: 'Terracina', 2285: 'seat', 8589: 'sites;'}


def test_parse_sentence_diff():
    sentence_diff_line = '> -19752 -19307 -1006 -14 -8590 -2286 -24766 Chu on. 110 cc269d'
    cdiff = CDiffFile._parse_sentence_diff(sentence_diff_line)

    assert cdiff == CDiff(positions=[-19752, -19307, -1006, -14, -8590, -2286, -24766],
                          start_trigram='Chu',
                          end_trigram='on.',
                          sentence_length='110',
                          sentence_hash='cc269d')


