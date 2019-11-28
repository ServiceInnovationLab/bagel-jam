import json
from glob import glob
import csv

INPUT_FILE_PATTERN = 'input/*.txt'
INPUT_FOLDER_NAME = 'input/'
OUTPUT_FOLDER_NAME = '../docs/'
SENTIMENT_ANALYSIS_FILE = 'sentiment-analysis/output.json'
DOC_TOPICS_FILE = 'topic-modelling/doc-topics.csv'
TOPIC_TERMS_FILE = 'topic-modelling/topic-terms.csv'
KEY_PHRASES_FILE = 'key-phrases/key-phrases.json'

def sort_by_line_number(elem):
    return elem['line_number']

def sort_by_weight(elem):
    return elem['weight']

def key_phrases_for_submission(filename):
    if INPUT_FOLDER_NAME in filename:
        input_file_name = filename
        filename = filename.replace(INPUT_FOLDER_NAME, '')
    else:
        input_file_name = INPUT_FOLDER_NAME + filename

    p = KEY_PHRASES.get(filename, None)
    return(p)

def topics_for_submission(filename):
    if INPUT_FOLDER_NAME in filename:
        input_file_name = filename
        filename = filename.replace(INPUT_FOLDER_NAME, '')
    else:
        input_file_name = INPUT_FOLDER_NAME + filename

    return(docs_with_topics.get(filename, None))

def sentiment_analysis_for_submission(filename):
    if INPUT_FOLDER_NAME in filename:
        input_file_name = filename
        filename = filename.replace(INPUT_FOLDER_NAME, '')
    else:
        input_file_name = INPUT_FOLDER_NAME + filename

    sentiment = sentiment_analysis[filename]

    with open(input_file_name) as f:
        submission_contents = f.readlines()

    labelled_line_numbers = []

    for l in sentiment:
        line_number = l['Line']

        sentiment_details = {}

        predicted_sentiment = l['Sentiment']
        sentiment_details['sentiment'] = predicted_sentiment.lower()
        sentiment_details['confidence'] = l['SentimentScore'][predicted_sentiment.title()]

        line_details = {}

        line_details['line_number'] = line_number
        line_details['original_text'] = submission_contents[line_number]
        line_details['sentiment'] = sentiment_details

        labelled_line_numbers.append(line_details)


    return(sorted(labelled_line_numbers, key=sort_by_line_number))

def everything_for_file(filename):
    sentiment = sentiment_analysis_for_submission(filename)
    key_phrases = key_phrases_for_submission(filename)
    topics = topics_for_submission(filename)
    return({'sentiment': sentiment, 'key_phrases': key_phrases, 'topics': topics})

FILENAMES = glob(INPUT_FILE_PATTERN)

# Import key phrases
with open(KEY_PHRASES_FILE) as f:
    contents = f.read()

RAW_KEY_PHRASES = json.loads(contents)
KEY_PHRASES = {}

for item in RAW_KEY_PHRASES:
    filename = item['File']
    if KEY_PHRASES.get(filename, None) is None:
        KEY_PHRASES[filename] = []
    phrases = item['KeyPhrases']
    for phrase in phrases:
        phrase.pop('BeginOffset')
        phrase.pop('EndOffset')
    KEY_PHRASES[filename] = phrases

# Import sentiment analysis

with open(SENTIMENT_ANALYSIS_FILE) as f:
    contents = f.read()

raw_sentiment_analysis = json.loads(contents)
sentiment_analysis = {}

for item in raw_sentiment_analysis:
    filename = item['File']
    if sentiment_analysis.get(filename, None) is None:
        sentiment_analysis[filename] = []
    sentiment_analysis[filename].append(item)

# Import topic modelling: topics

topic_terms = {}

with open(TOPIC_TERMS_FILE, newline='') as topic_terms_file:
    reader = csv.reader(topic_terms_file, delimiter=',')
    for row in reader:
        if row[0] == 'topic':
            next
        else:
            topic_number = row[0]
            item = {'term': row[1], 'weight': row[2]}
            if topic_terms.get(topic_number, None) is None:
                topic_terms[topic_number] = []
            topic_terms[topic_number].append(item)

for key, value in topic_terms.items():
    topic_terms[key] = sorted(value, key=sort_by_weight, reverse=True)


# Import topic modelling: documents

docs_with_topics = {}

with open(DOC_TOPICS_FILE, newline='') as doc_topics:
    reader = csv.reader(doc_topics, delimiter=',')
    for row in reader:
        if row[0] == 'docname':
            next
        else:
            filename = row[0]
            item = {'topic': row[1], 'confidence': row[2]}

            if docs_with_topics.get(filename, None) is None:
                docs_with_topics[filename] = []
            docs_with_topics[filename].append(item)

FILE_NAMES_ONLY = []

for filename in FILENAMES:
    print(filename)
    FILE_NAMES_ONLY.append(filename.replace(INPUT_FOLDER_NAME, ''))

    data = everything_for_file(filename)
    destination = filename.replace(INPUT_FOLDER_NAME, OUTPUT_FOLDER_NAME)
    with open(destination, 'w') as outfile:
        json.dump(data, outfile)

with open("{folder}/{file}.json".format(folder=OUTPUT_FOLDER_NAME, file='topics'), 'w') as outfile:
    json.dump(topic_terms, outfile)

with open("{folder}/{file}.json".format(folder=OUTPUT_FOLDER_NAME, file='meta'), 'w') as outfile:
    json.dump(FILE_NAMES_ONLY, outfile)
