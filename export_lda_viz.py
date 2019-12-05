from bagel.viz.viz import export_lda_viz

FILE_PATTERN = 'zero-carbon-bill/input/*.txt'
# Tweak this parameter until it brings joy
NUMBER_OF_TOPICS = 5
OUTPUT_PATH = 'docs/index_lda.html'

export_lda_viz(NUMBER_OF_TOPICS, FILE_PATTERN, OUTPUT_PATH)
