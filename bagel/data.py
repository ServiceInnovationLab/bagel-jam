#!/usr/bin/env python

from glob import glob
import re
import gensim
from gensim.utils import simple_preprocess


class DataSet(object):
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

    def files_with_words(self, words):
        for filename, data_file in self.files.items():
            word_found = False
            for word in words:
                if (word in data_file.cleaned_data):
                    word_found = True
            if word_found:
                yield(filename)


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
        self.words = gensim.utils.simple_preprocess(
            self.cleaned_data, deacc=True)

if __name__ == "__main__":
    dataset = DataSet('zero-carbon-bill/input/*.json')