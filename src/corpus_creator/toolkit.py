#!/usr/bin/env python
# encoding: utf-8

'''
Helper functions

::author: Albert Weichselbraun <albert@weichselbraun.net>
'''


def find_all(text, substring):
    ''' 
    :: returns all matches of substring in text.
    '''
    start = 0
    while True:
        start = text.find(substring, start)
        if start == -1:
            return
        yield start
        start += 1


def get_resource(url):
    ''' returns the content of the given resource '''
    if url.startswith('http://') or url.startswith('https://'):
        # We currently do not support Web resources
        return ''

    with open(url) as f:
        return f.read().decode("utf-8")
