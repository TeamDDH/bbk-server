# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import jieba.analyse
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from .db import SpiderArticle, ServerArticle, ServerTopic

import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt


def load_stop_words():
    return [line.decode('utf-8').strip() for line in open('./algorithm/stop.txt', 'r').readlines()]


def load_data_set():
    def extract_content(article):
        return article.content

    def cut_text(text):
        words = list(jieba.cut(text, cut_all=False))
        ots = ''
        for word in words:
            if word not in stopwords and word != 't':
                ots += word
                ots += ' '
        return ots

    print('[INFO] loading stop words vocabulary...')
    stopwords = load_stop_words()
    articles = SpiderArticle.get_all_articles()
    contents = map(extract_content, articles)
    cut_content = map(cut_text, contents)
    return articles, cut_content


def transform(dataset):
    """Generate VSM from extracted keywords."""

    print('[INFO] Generating VSM...')

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()

    tfidf = transformer.fit_transform(vectorizer.fit_transform(dataset))
    weight = tfidf.toarray()

    return weight


def train(weight, true_k=10):
    print('[INFO] traning with K=', true_k)

    clf = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1)
    clf.fit(weight)
    result = list(clf.predict(weight))
    return result, -clf.score(weight)


def test():
    """A method to show how error rate decreases with k increasing."""
    dataset = load_data_set()
    weight = transform(dataset)
    true_ks = []
    scores = []

    for i in xrange(100, 105, 1):
        result, score = train(weight, true_k=i)
        true_ks.append(i)
        scores.append(score / len(dataset))

    plt.figure(figsize=(8, 4))
    plt.plot(true_ks, scores, label="error", color="red", linewidth=1)
    plt.xlabel("n_features")
    plt.ylabel("error")
    plt.legend()
    plt.show()


def start():
    """Seriously!"""
    articles, dataset = load_data_set()
    weight = transform(dataset)

    result, score = train(weight, true_k=180)

    clusters = {}
    n = 0
    for item in result:
        if item in clusters:
            clusters[item].append(n)
        else:
            clusters[item] = [n]
        n += 1

    store_all(articles, clusters)


def store_all(articles, clusters):
    article_id_lists = clusters.values()

    for line in article_id_lists:
        typical_article = articles[line[0]]
        new_topic = ServerTopic.insert_a_topic(typical_article.title)

        for index in line:
            new_article = articles[index]
            ServerArticle.insert_an_article(title=new_article.title, uri=new_article.uri, topic_id=new_topic._id)
