import json
from glob import glob
import csv

def sort_by_line_number(elem):
    return elem['line_number']

def sort_by_weight(elem):
    return elem['weight']

input_file_pattern = 'input/*.json'
input_folder_name = 'input/'
output_folder_name = 'combined/'

filenames = glob(input_file_pattern)

# Import key phrases
key_phrases_file = 'key-phrases/key-phrases.json'
with open(key_phrases_file) as f:
    contents = f.read()

raw_key_phrases = json.loads(contents)
key_phrases = {}

for item in raw_key_phrases:
    filename = item['File']
    if key_phrases.get(filename, None) is None:
        key_phrases[filename] = []
    phrases = item['KeyPhrases']
    for phrase in phrases:
        phrase.pop('BeginOffset')
        phrase.pop('EndOffset')
    key_phrases[filename] = phrases

# Import sentiment analysis

sentiment_analysis_file = 'sentiment-analysis/output.json'
with open(sentiment_analysis_file) as f:
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

with open('topic-modelling/topic-terms.csv', newline='') as topic_terms_file:
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

with open('topic-modelling/doc-topics.csv', newline='') as doc_topics:
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

def key_phrases_for_submission(filename):
    if input_folder_name in filename:
        input_file_name = filename
        filename = filename.replace(input_folder_name, '')
    else:
        input_file_name = input_folder_name + filename

    p = key_phrases.get(filename, None)
    return(p)

def topics_for_submission(filename):
    if input_folder_name in filename:
        input_file_name = filename
        filename = filename.replace(input_folder_name, '')
    else:
        input_file_name = input_folder_name + filename

    return(docs_with_topics.get(filename, None))

def sentiment_analysis_for_submission(filename):
    if input_folder_name in filename:
        input_file_name = filename
        filename = filename.replace(input_folder_name, '')
    else:
        input_file_name = input_folder_name + filename

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

for filename in filenames:
    print(filename)
    data = everything_for_file(filename)
    destination = filename.replace(input_folder_name, output_folder_name)
    with open(destination, 'w') as outfile:
        json.dump(data, outfile)

with open(output_folder_name + 'topics.json', 'w') as outfile:
    json.dump(topic_terms, outfile)
