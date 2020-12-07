from string import punctuation
from nltk.corpus.reader.util import find_corpus_fileids
from pymystem3 import Mystem
from nltk.corpus import stopwords
import nltk
from flask import Flask, request, jsonify
import requests
app_key = ""

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# download stopwords corpus, you need to run it once
nltk.download("stopwords")
#--------#
# Create lemmatizer and stopwords list
mystem = Mystem()
russian_stopwords = stopwords.words("russian")
# Preprocess function


def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords
              and token != " "
              and token.strip() not in punctuation
              and not token.strip().isdigit()]
    return tokens


def translate(words):
    translated = {}
    for word in words:
        translated.setdefault(word, '')
        source_language_code = "ru"
        target_language_code = "en"
        url = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=" + \
            app_key + "&lang=" + source_language_code + "-" + \
            target_language_code + "&text=" + word.lower()
        r = requests.post(url)
        response_data = r.json()
        try:
            translated[word] = response_data['def'][0]['tr'][0]['text']
        except:
            continue
    return translated


def checkLevel(text, level):
    filepath_a1 = './assets/lex_minimum_a1.txt'
    dataset = set(text)
    if len(dataset) == 0:
        return
    words_a1 = set()
    with open(filepath_a1) as fp:
        for line in fp:
            words_a1.add(line.rstrip())
    if level == 'a1':
        return len(dataset.intersection(words_a1)) / len(dataset)
    filepath_a2 = './assets/lex_minimum_a2.txt'
    words_a2 = set()
    with open(filepath_a2) as fp:
        for line in fp:
            words_a2.add(line.rstrip())
    return len(dataset.intersection(words_a2)) / len(dataset)


def countWords(words):
    counted = {}
    for word in words:
        counted.setdefault(word, 0)
        counted[word] += 1
    return counted


def checkFrequency(text):
    x = countWords(text)
    res = {k: v for k, v in sorted(
        x.items(), key=lambda item: item[1], reverse=True)}
    return res


def findIntersection(text1, text2):
    text1_set = set(text1)
    text2_set = set(text2)
    inters = text1_set.intersection(text2_set)
    return sorted(list(inters))


def getSortedList(text):
    return sorted(list(set(text)))


@app.route('/api/', methods=["POST"])
def main_interface():
    response = request.get_json()
    result = {}
    text1 = sorted(preprocess_text(response['text1']))
    text2 = sorted(preprocess_text(response['text2']))
    result['text1'] = getSortedList(text1)
    result['text2'] = getSortedList(text2)
    result['intersection'] = []
    if len(text2) > 0:
        result['intersection'] = findIntersection(text1, text2)
    return jsonify(result)


@app.route('/api/freq/', methods=["POST"])
def freq_interface():
    response = request.get_json()
    result = {}
    text1 = sorted(preprocess_text(response['text1']))
    text2 = sorted(preprocess_text(response['text2']))
    result['text1'] = checkFrequency(text1)
    result['text2'] = checkFrequency(text2)
    result['intersection'] = []
    if len(text2) > 0:
        result['intersection'] = findIntersection(text1, text2)
    return jsonify(result)


@app.route('/api/lex/', methods=["POST"])
def lex_interface():
    response = request.get_json()
    result = {}
    text1 = sorted(preprocess_text(response['text1']))
    text2 = sorted(preprocess_text(response['text2']))
    result['text1'] = getSortedList(text1)
    result['text2'] = getSortedList(text2)
    result['text1_a1'] = ''
    result['text1_a2'] = ''
    result['text2_a1'] = ''
    result['text2_a2'] = ''
    result['text1_a1'] = checkLevel(text1, 'a1')
    result['text1_a2'] = checkLevel(text1, 'a2')
    result['text2_a1'] = checkLevel(text2, 'a1')
    result['text2_a2'] = checkLevel(text2, 'a2')
    result['intersection'] = []
    if len(text2) > 0:
        result['intersection'] = findIntersection(text1, text2)
    return jsonify(result)


@app.route('/api/dict/', methods=["POST"])
def dict_interface():
    response = request.get_json()
    result = {}
    text1 = sorted(preprocess_text(response['text1']))
    text2 = sorted(preprocess_text(response['text2']))
    result['text1'] = translate(getSortedList(text1))
    result['text2'] = translate(getSortedList(text2))
    result['intersection'] = []
    if len(text2) > 0:
        result['intersection'] = findIntersection(text1, text2)
    return jsonify(result)


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    return response


if __name__ == '__main__':
    app.run(debug=True)
