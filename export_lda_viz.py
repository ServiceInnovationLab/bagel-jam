from bagel.viz.export import export_lda_viz

FILE_PATTERN = 'zero-carbon-bill/input/*.txt'
# Tweak this parameter until it brings joy
NUMBER_OF_TOPICS = 10
OUTPUT_PATH = 'docs/lda/index.html'

if __name__ == "__main__":
    export_lda_viz(NUMBER_OF_TOPICS, FILE_PATTERN, OUTPUT_PATH)
