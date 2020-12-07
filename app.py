from string import punctuation
from pymystem3 import Mystem
from nltk.corpus import stopwords
import nltk
from flask import Flask, request, jsonify
import requests
app_key = ""

app = Flask(__name__)

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


def count_words(words):
    counted = {}
    for word in words:
        counted.setdefault(word, 0)
        counted[word] += 1
    return counted


def transl(words):
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


@app.route('/api/', methods=["POST"])
def main_interface():
    response = request.get_json()
    result = {}
    result1 = sorted(preprocess_text(response['text1']))
    result2 = sorted(preprocess_text(response['text2']))
    result1_set = set(result1)
    result2_set = set(result2)
    checkboxLevel = response['checkboxLevel']
    if checkboxLevel:
        filepath_a1 = '/home/johanla0/mysite/assets/lex_minimum_a1.txt'
        filepath_a2 = '/home/johanla0/mysite/assets/lex_minimum_a2.txt'
        words_a1 = set()
        words_a2 = set()
        with open(filepath_a1) as fp:
            for line in fp:
                words_a1.add(line.rstrip())
        with open(filepath_a2) as fp:
            for line in fp:
                words_a2.add(line.rstrip())
        result['result1_a1'] = ''
        result['result1_a2'] = ''
        result['result2_a1'] = ''
        result['result2_a2'] = ''
        if len(result1_set) > 0:
            result['result1_a1'] = len(
                result1_set.intersection(words_a1)) / len(result1_set)
            result['result1_a2'] = len(
                result1_set.intersection(words_a2)) / len(result1_set)
        if len(result2_set) > 0:
            result['result2_a1'] = len(
                result2_set.intersection(words_a1)) / len(result2_set)
            result['result2_a2'] = len(
                result2_set.intersection(words_a2)) / len(result2_set)
    checkboxFrequency = response['checkboxFrequency']
    checkboxTranslate = response['checkboxTranslate']
    if checkboxFrequency:
        result['result1'] = count_words(result1)
        result['result2'] = count_words(result2)
    else:
        result['result1'] = sorted(list(result1_set))
        result['result2'] = sorted(list(result2_set))
    if checkboxTranslate:
        result['result1'] = transl(sorted(list(result1_set)))
        result['result2'] = transl(sorted(list(result2_set)))
    result['intersection'] = []
    if len(result2) > 0:
        inters = result1_set.intersection(result2_set)
        result['intersection'] = sorted(list(inters))
    return jsonify(result)


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    return response


if __name__ == '__main__':
    app.run(debug=True)
