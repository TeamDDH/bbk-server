# -*- coding: utf-8 -*-
"""
    algorithm
    ~~~~~~~~~

    The algorithm core of bbk system.

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

import json
from tfidf import TFIDF


class Analyzer(object):
    """Analyzer is the organizer of the processing."""

    def __init__(self):
        self.tfidf = TFIDF()

    def analyze_text(self, text):
        """This methods receives the content of a given article, and go through
        the analyzing process includes:
        - tfidf as pre-processing
        - comparing similaries with existing topics
        """
        pass


if __name__ == '__main__':
    ana = Analyzer()
    article = open('./tfidfsample.txt').read()
    words = ana.tfidf.get_keywords_from_text(article)
    print json.dumps(words).decode('unicode-escape')
