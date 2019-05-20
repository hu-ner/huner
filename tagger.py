#!/usr/bin/env python

from __future__ import print_function


import os
from flask import Flask, request, jsonify, session
import time
import codecs
import optparse
import numpy as np
from loader import prepare_sentence
from utils import create_input, iobes_iob, zero_digits
from model import Model
import sys
import logging
from opennlp_wrapper import SentenceSplitter, OpenNLP

app = Flask(__name__)

model = Model(model_path="/usr/huner/models/" + sys.argv[1])
sentence_splitter = SentenceSplitter(os.getenv('OPENNLP'), 'en-sent.bin')
tokenizer = OpenNLP(os.getenv('OPENNLP'), 'TokenizerME', 'en-token.bin')
parameters = model.parameters


def split_sentences(text):
    text = '\n'.join(text)
    text = text.strip()
    return sentence_splitter.split(text)


def tokenize(sentence): 
    sentence = sentence.strip()
    return tokenizer.parse(sentence).decode().split()


# Load reverse mappings
word_to_id, char_to_id, tag_to_id = [
    {v: k for k, v in x.items()}
    for x in [model.id_to_word, model.id_to_char, model.id_to_tag]
]

# Load the model
_, f_eval = model.build(training=False, **parameters)
model.reload()

@app.route("/tag", methods=["POST"])
def tag():
    if request.method == 'POST':
        data = request.get_json()
        text = data['text']
        if data['split_sentences']:
            sentences = split_sentences(text)
        else:
            sentences = text

        if data['tokenize'] or data['split_sentences']:
            tokenized_sentences = [tokenize(s) for s in sentences]
        else:
            tokenized_sentences = text


        count = 0
        output = []
        for words in tokenized_sentences:
            if len(words) == 0:
                continue
            # Lowercase sentence
            if model.parameters['lower']:
                line = line.lower()
            # Replace all digits with zeros
            if model.parameters['zeros']:
                line = zero_digits(line)
            # Prepare input
            sentence = prepare_sentence(words, word_to_id, char_to_id,
                                        lower=model.parameters['lower'])
            input = create_input(sentence, model.parameters, False)
            # Decoding
            if model.parameters['crf']:
                y_preds = np.array(f_eval(*input))[1:-1]
            else:
                y_preds = f_eval(*input).argmax(axis=1)
            y_preds = [model.id_to_tag[y_pred] for y_pred in y_preds]
            # Output tags in the IOB2 format
            if model.parameters['tag_scheme'] == 'iobes':
                y_preds = iobes_iob(y_preds)
            # Write tags
            assert len(y_preds) == len(words), "Predictions have different length than sentence. Something went wrong."
            output.append(list(zip(words, y_preds)))
            count += 1
            if count % 100 == 0:
                logging.info(count)

        return jsonify(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
