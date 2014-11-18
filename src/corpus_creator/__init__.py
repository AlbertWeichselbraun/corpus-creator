#!/usr/bin/env python
# encoding: utf-8

from html2text import HTML2Text
from hashlib import md5

# computes a 24 bit checksum
checksum = lambda text: md5(text.encode("utf8")).hexdigest()[:6]

# provides get_text support
h = HTML2Text()
h.ignore_links = True
h.ignore_images = True
h.body_width = 0

def get_text(html):
    ''' converts the given html to text '''
    return h.handle(html)

