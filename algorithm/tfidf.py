# -*- coding: utf-8 -*-
"""
    tdidf
    ~~~~~

    Compare two articles using td-idf and cosine.

    :copyright: (c) 2017-18 by Wendell Hu.
    :license: MIT, see LICENSE for more details.
"""

import jieba.analyse

from config import NUM_OF_KEYWORDS


class TFIDF(object):
    #: TODO: later we could setup an IDF file and stop words file.
    def __init__(self):
        pass

    def get_keywords_from_text(self, text):
        return jieba.analyse.extract_tags(text,
                                          topK=NUM_OF_KEYWORDS,
                                          withWeight=True)
