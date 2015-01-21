#!/usr/bin/env python
# encoding: utf-8

''' 
test-corpus-restore

::author: Albert Weichselbraun <albert@weichselbraun.net>
'''

from os.path import dirname, join as os_join

from corpus_creator.corpus_restore import corpus_restore, extract_sentence_from_trigram

TEST_DIR = dirname(__file__)
INPUT_HTML = ('Chur.html', 'Chur_modified1.html', )# 'Chur_modified2.html')
INPUT_CDIFF = 'Chur.cdiff'
CORPUS_FILE = 'Chur.txt'

def test_extract_sentence_from_trigram():
    sentence, is_valid = extract_sentence_from_trigram(
        from_text = u"Hallo wie geht's. Das ist gut! Das macht Mut! Das tut gut! Tschau :)",
        sentence_len = 12,
        start_trigram = 'Das',
        end_trigram = 'ut!',
        sentence_hash = 'e09792')

    assert sentence == 'Das tut gut!'
    assert is_valid

    # test encoding
    sentence, is_valid = extract_sentence_from_trigram(
        from_text = u"""This is a text snippet which has been inserted to test the robustness of our methods 
Chur or Coire[3] is the capital of the Swiss canton of Graubünden and lies in the northern part of the canton. The city, which is located on the right bank of the Rhine River, is reputedly the oldest town of Switzerland.""",
        sentence_len = 110,
        start_trigram = u'Chu',
        end_trigram = u'on.',
        sentence_hash = 'cc269d')


def test_corpus_restore():
    ''' test the corpus restore sequence '''
    with open(os_join(TEST_DIR, CORPUS_FILE)) as f:
        reference_sentences = f.read().decode("utf-8").strip()

    for input_file in INPUT_HTML:
        sentences = corpus_restore(diff_file=os_join(TEST_DIR, INPUT_CDIFF), 
            working_directory=TEST_DIR, html_url=input_file)

        assert sentences == reference_sentences
