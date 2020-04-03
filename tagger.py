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
_, f_eval, f_conf = model.build(training=False, **parameters)
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
                alpha_masks = pred_to_alpha_masks(y_preds, {v: k for k, v in model.id_to_tag.items()}, model.id_to_tag)
                confidences_per_entity = []
                for alpha_mask in alpha_masks:
                    conf_input = input + [alpha_mask]
                    conf = np.array(f_conf(*conf_input))
                    confidences_per_entity.append(float(np.exp(conf)))
            else:
                raise NotImplementedError
                # y_preds = f_eval(*input).argmax(axis=1)
            y_preds = [model.id_to_tag[y_pred] for y_pred in y_preds]
            # Output tags in the IOB2 format
            if model.parameters['tag_scheme'] == 'iobes':
                y_preds = iobes_iob(y_preds)
            # Write tags
            assert len(y_preds) == len(words), "Predictions have different length than sentence. Something went wrong."
            confidences = []
            for word, tag in zip(words, y_preds):
                if tag.startswith('B'):
                    confidence = confidences_per_entity.pop(0)
                else:
                    confidence = None
                confidences.append(confidence)
            output.append(list(zip(words, y_preds, confidences)))
            count += 1
            if count % 100 == 0:
                logging.info(count)

        return jsonify(output)

def pred_to_alpha_masks(y_pred, label_to_index, index_to_label, epsilon=1e-7):
    """
    y_pred $\in \{0, .., n_tags-1\}^{seq_len} are the predicted tags for one example
    We assume that only valid tag-transitions are predicted
    """

    masks = []
    prev_label = None
    i_label_index = None
    mask = None
    for seq_idx, label_idx in enumerate(y_pred):
        label = index_to_label[label_idx]

        # enforce negative constraints
        if prev_label is not None and prev_label != 'O' and (label == 'O' or label.startswith('B') or label.startswith('S')):
            mask[seq_idx, i_label_index] = 0
            masks.append(mask + epsilon)
            mask = None

        if label.startswith('B') or label.startswith('S'):
            mask = np.ones((len(y_pred)+2, len(label_to_index)+2), dtype='float32')
            relevant_b_label = label
            i_label_index = label_to_index['I' + relevant_b_label[1:]]

        # enforce positive constraints
        if label != 'O':
            # try:
            mask[seq_idx, :] = 0
            mask[seq_idx, label_idx] = 1
            # except TypeError:
            # import IPython; IPython.embed()

        prev_label = label

    if mask is not None:
        masks.append(mask + epsilon)

    return masks

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, use_reloader=True)
