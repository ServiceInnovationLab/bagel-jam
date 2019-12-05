#!/usr/bin/env python
from bagel import DataSet, DataFile
import pyLDAvis.gensim

def export_lda_viz(num_topics, file_pattern, output_path):
    dataset = DataSet(glob=file_pattern, num_topics=num_topics)
    dataset.make_lda_model()

    lda_display = pyLDAvis.gensim.prepare(dataset.lda_model, dataset.corpus, dataset.dictionary, sort_topics=False)
    pyLDAvis.save_html(lda_display, output_path)
