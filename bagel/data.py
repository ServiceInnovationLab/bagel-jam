#!/usr/bin/env python

from glob import glob
import re
import gensim
from gensim.utils import simple_preprocess
from gensim import corpora, models

from nltk.corpus import stopwords


class DataSet(object):
    TOKEN_PATTERN = r'\b[a-zA-ZāēīōūĀĒĪŌŪ]{3,}\b'

    def __init__(self, glob):
        self._glob = glob
        self.files = {}
        self.input_data = {}
        for filename in self.filenames:
            self.files[filename] = DataFile(filename)

    @property
    def all_input_data(self):
        for filename, data_file in self.files.items():
            yield(data_file.input_data)

    @property
    def filenames(self):
        return glob(self._glob)

    def make_lda_model(self):
        """
        Converts the documents into a matrix of features
         features are interesting words
         https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
        """

        list_of_list_of_tokens = []
        for filename, data_file in self.files.items():
            list_of_list_of_tokens.append(data_file.words)

        self.dictionary_LDA = corpora.Dictionary(list_of_list_of_tokens)
        self.dictionary_LDA.filter_extremes(no_below=3, no_above=0.9)
        self.corpus = [self.dictionary_LDA.doc2bow(
            list_of_tokens) for list_of_tokens in list_of_list_of_tokens]
        num_topics = 20
        self.lda_model = models.LdaModel(self.corpus, num_topics=num_topics,
                                         id2word=self.dictionary_LDA,
                                         passes=4, alpha=[0.01]*num_topics,
                                         eta=[0.01]*len(self.dictionary_LDA.keys()))

    @property
    def cleaned_data(self):
        for filename, data_file in self.files.items():
            lda_model[self.dictionary_LDA.doc2bow(data_file.words)]
            print(filename)
            print('---------------------')

    def print_topics(self, num_topics, num_words):
        self.topics = {}
        for i, topic in self.lda_model.show_topics(formatted=True, num_topics=num_topics, num_words=10):
            print(str(i)+": " + topic)
            percent = (self.lda_model[self.corpus[i]][0][1] * 100)
            print("{percent:.2f}% of the data is in this topic".format(
                percent=percent))
            print()

    def print_files(self):
        for filename, data_file in self.files.items():
            model = self.lda_model[self.dictionary_LDA.doc2bow(
                data_file.words)]
            print("{percent:2.2f}% in topic {topic_number}.\t{filename}".format(
                filename=filename,
                percent=model[0][1] * 100,
                topic_number=model[0][0]))


class DataFile(object):
    regexp = "[,\\.!?]"

    def __init__(self, filename):
        self._filename = filename
        with open(filename) as f:
            self.input_data = f.read()
        self.clean()
        self.split_into_words()

    def clean(self):
        self.cleaned_data = self.input_data.lower()
        # Remove punctuation
        self.cleaned_data = re.sub(self.regexp, '', self.cleaned_data)
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
    dataset.print_topics(num_topics=20, num_words=15)
    dataset.print_files()
