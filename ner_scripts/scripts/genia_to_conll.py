import argparse

from bs4 import BeautifulSoup
from tqdm import tqdm

import utils


def is_named_entity(entity):
    try:
        return entity['sem'] in {
            'G#protein_molecule',
            'G#protein_family_or_group'
        }

    except KeyError:
        return False


def extract_sentence_info(sentence):
    """
    :param sentence:
    :return:
    """
    sentence_text = []
    sentence_entities = []

    def helper(entity):
        if hasattr(entity, "children"):
            if is_named_entity(entity):
                # Hack around immutable strings + scoping mechanisms
                # (see https://stackoverflow.com/questions/5218895/python-nested-functions-variable-scoping)
                text = "".join(sentence_text)
                entity_start = len(text)
                sentence_text.append(entity.get_text())
                entity_end = len(text) + len(entity.get_text())
                sentence_entities.append((entity_start, entity_end))
            else:
                for child in entity.children:
                    helper(child)
        else:
            sentence_text.append(entity)

    for child in sentence.children:
        helper(child)

    return "".join(sentence_text), sentence_entities

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    all_sentences = []
    all_entities = []

    with open(args.input, 'r') as f_in:
        soup = BeautifulSoup(f_in, 'lxml')
        for sentence in tqdm(soup.find_all('sentence')):
            sentence_text, sentence_entities = extract_sentence_info(sentence)
            all_sentences.append(sentence_text)
            all_entities.append(sentence_entities)

    with open(args.output, 'w') as f_out:
        utils.write_to_conll(all_sentences, all_entities, f_out)
