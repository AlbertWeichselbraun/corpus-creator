#!/usr/bin/env python
# encoding: utf-8

'''
Helper functions

::author: Albert Weichselbraun <albert@weichselbraun.net>
'''
from urllib2 import urlopen

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
    ''' returns the content of the given resource 
    
    :param url: \
        the web or local url of the resource.
    :returns: \
        the resource's content
    '''
    if url.startswith('http://') or url.startswith('https://'):
        f = urlopen(url)
        return f.read().decode('utf-8')

    with open(url) as f:
        return f.read().decode('utf-8')
