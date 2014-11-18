#!/usr/bin/env python
# encoding: utf-8

''' 
test-corpus-restore

::author: Albert Weichselbraun <albert@weichselbraun.net>
'''

from os.path import dirname

from corpus_creator.corpus_restore import corpus_restore, extract_sentence_from_trigram

TEST_DIR = dirname(__file__)
INPUT_HTML = ('Chur.html', )
INPUT_CDIFF = 'Chur.cdiff'
CORPUS_FILE = 'Chur.txt'

def test_extract_sentence_from_trigram():
    sentence, is_valid = extract_sentence_from_trigram(
        from_text = "Hallo wie geht's. Das ist gut! Das macht Mut! Das tut gut! Tschau :)",
        sentence_len = 12,
        start_trigram = 'Das',
        end_trigram = 'ut!',
        sentence_hash = 'e09792')

    assert sentence == 'Das tut gut!'
    assert is_valid


def test_corpus_restore():
    ''' test the corpus restore sequence '''
    with open(CORPUS_FILE) as f:
        reference_sentences = f.read().decode("utf-8").strip()

    for input_files in INPUT_HTML:
        sentences = corpus_restore(diff_file=INPUT_CDIFF, 
            working_directory=TEST_DIR, html_url=input_files)

        assert sentences == reference_sentences
    

