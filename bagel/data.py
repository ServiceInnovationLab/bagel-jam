#!/usr/bin/env python

from glob import glob
import re
import gensim
from gensim.utils import simple_preprocess
from gensim import corpora, models

from nltk.corpus import stopwords


class DataSet(object):
    TOKEN_PATTERN = r'\b[0-9a-zA-ZāēīōūĀĒĪŌŪ]{3,}\b'

    def __init__(self, glob, num_topics):
        self._glob = glob
        self.num_topics = num_topics
        self.files = {}
        self.input_data = {}
        for filename in self.filenames:
            self.files[filename] = DataFile(filename)

    @property
    def filenames(self):
        return glob(self._glob)

    @property
    def list_of_list_of_tokens(self):
        return [data_file.words for filename, data_file in self.files.items()]

    @property
    def all_tokens(self):
        for filename, data_file in self.files.items():
            for word in data_file.words:
                yield word

    def make_lda_model(self):
        """
        Converts the documents into a matrix of features.
         Features are interesting words
         https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
        """

        self.dictionary = corpora.Dictionary(self.list_of_list_of_tokens)
        self.dictionary.filter_extremes(no_below=3, no_above=0.8)
        self.corpus = [self.dictionary.doc2bow(
            list_of_tokens) for list_of_tokens in self.list_of_list_of_tokens]
        self.lda_model = models.LdaModel(self.corpus, num_topics=self.num_topics,
                                         id2word=self.dictionary,
                                         passes=4, alpha=[0.01]*self.num_topics,
                                         eta=[0.01]*len(self.dictionary.keys()))

    @property
    def cleaned_data(self):
        for filename, data_file in self.files.items():
            lda_model[self.dictionary.doc2bow(data_file.words)]
            print(filename)
            print('---------------------')

    def print_topics(self, num_words):
        self.topics = {}
        for i, topic in self.lda_model.show_topics(
                formatted=True,
                num_topics=self.num_topics,
                num_words=num_words):
            print(str(i)+": " + topic)
            percent = (self.lda_model[self.corpus[i]][0][1] * 100)
            print("{percent:.2f}% of the data is in this topic".format(
                percent=percent))
            print()
            self.topics[i] = topic

    def print_files(self):
        for item in self.file_topics():
            print("{percent:2.2f}% in topic {topic_number}.\t{filename}".format(
                filename=item['filename'],
                percent=item['percent'],
                topic_number=item['topic_idx']))
            print("TOPICS: {}".format(item['topic']))
            print(self.files[item['filename']].cleaned_data)
            print('-----------------------')
            print()

    def file_topics(self):
        for filename, data_file in self.files.items():
            file_idx = self.dictionary.doc2bow(data_file.words)
            model = self.lda_model[file_idx]
            topic_idx = model[0][0]
            percent = model[0][1] * 100
            topic = self.topics.get(topic_idx)
            yield({
                'filename': filename,
                'percent': percent,
                'topic_idx': topic_idx,
                'topic': topic})


class DataFile(object):
    def __init__(self, filename):
        self._filename = filename
        with open(filename) as f:
            self.input_data = f.read()
        self.clean()
        self.split_into_words()

    def clean(self):
        self.cleaned_data = self.input_data.lower()
        # joins some phrases
        self.cleaned_data = self.cleaned_data.replace(
            'new zealand', 'newzealand')

    def split_into_words(self):
        words = gensim.utils.simple_preprocess(self.cleaned_data, deacc=True)
        stop_words = stopwords.words('english')
        self.words = [word for word in words if word not in stop_words]


if __name__ == "__main__":
    dataset = DataSet('zero-carbon-bill/input/*.json')
    dataset.make_lda_model()
    dataset.print_topics(num_topics=10, num_words=5)
    dataset.print_files()
