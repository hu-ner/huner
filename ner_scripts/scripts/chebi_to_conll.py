import argparse
from glob import glob
from tqdm import tqdm

import os
from bs4 import BeautifulSoup

import utils
from opennlp_wrapper import SentenceSplitter


def is_named_entity(entity):
    try:
        return entity['type'] in {
            'CHEMICAL',
            'FORMULA',
            'LIGAND',
            'CM',
            'CLASS'
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

    opennlp_path = os.environ['OPENNLP']
    sentence_splitter = SentenceSplitter(opennlp_path, 'en-sent.bin')

    all_sentences = []
    all_entities = []
    documents = glob(os.path.join(args.input, '**', '*.xml'))
    document_ids = []
    for document in tqdm(documents):
        with open(document, 'r') as f_in:
            soup = BeautifulSoup(f_in, 'lxml')
            for paragraph in soup.find_all('snippet'):
                if len(paragraph.text.strip()) == 0:
                    continue
                # each (new-line-separated) sentence seems to be valid html
                # so we extract the source, split at newline and parse again
                source = "".join(str(elem) for elem in paragraph.children)
                sentences = source.split('\n')
                for sentence in sentences:
                    document_id = os.path.basename(os.path.dirname(document))
                    sentence_bs = BeautifulSoup(sentence, 'lxml')
                    sentence_text, sentence_entities = extract_sentence_info(sentence_bs)
                    tmp_sentences = sentence_splitter.split(sentence_text)
                    tmp_entities = [[] for _ in tmp_sentences]
                    for entity in sentence_entities:
                        org_start = entity[0]
                        org_end = entity[1]
                        id, start, end = sentence_splitter.map_offsets(org_start, org_end)
                        while len(tmp_sentences[id]) < end:
                            tmp_sentences = sentence_splitter.merge_sentences(id)
                            tmp_entities[id] += tmp_entities[id + 1]
                            del tmp_entities[id + 1]
                            id, start, end = sentence_splitter.map_offsets(org_start, org_end)
                        tmp_entities[id] += [(start, end)]
                    all_sentences += tmp_sentences
                    all_entities += tmp_entities
                    document_ids += [document_id] * len(tmp_sentences)

    with open(args.output, 'w') as f_out:
        utils.write_to_conll(all_sentences, all_entities, document_ids, f_out)
