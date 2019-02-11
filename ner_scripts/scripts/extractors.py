import os
from lxml import etree
from tqdm import tqdm

from opennlp_wrapper import SentenceSplitter


opennlp_path = os.environ['OPENNLP']


def extract_from_biocreative(f, annotation_type, split_sentences=False) :
    sentence_splitter = SentenceSplitter(opennlp_path, 'en-sent.bin')
    tree = etree.parse(f)
    sentences = []
    entities = []
    document_ids = []
    documents = tree.xpath('.//document')

    for document in tqdm(documents):
        document_id = document.xpath('./id')[0].text
        passages = document.xpath('passage')
        uses_passage_offset = len(passages) > 1

        for passage in document.xpath('passage'):
            text = passage.xpath('text/text()')[0]

            if not split_sentences:
                tmp_sentences = text.split('\n')
            else:
                tmp_sentences = sentence_splitter.split(text)
            tmp_entities = [[] for _ in tmp_sentences]

            for annotation in passage.xpath('.//annotation'):
                # skip non-contiguous entities
                if len(annotation.xpath('.//location')) > 1:
                    continue

                is_entity = False

                for infon in annotation.xpath('.//infon'):
                    # Check if multiple types are given as a list
                    if type(annotation_type)==type(""):
                        is_entity |= ((infon.get('key') == 'type') & (infon.text == annotation_type))
                    else:
                        is_entity |= ((infon.get('key') == 'type') & (infon.text in annotation_type))
                if not is_entity:
                    continue
                offset = int(annotation.xpath('.//location')[0].get('offset'))
                if uses_passage_offset:
                    offset -= int(passage.xpath('./offset/text()')[0])
                length = int(annotation.xpath('.//location')[0].get('length'))
                if not split_sentences:
                    sentence_idx = 0
                    while offset > len(tmp_sentences[sentence_idx]):
                        offset -= len(tmp_sentences[sentence_idx])+1
                        sentence_idx += 1
                    end = offset + length
                else:
                    o_end = offset + length
                    o_offset = offset
                    sentence_idx, offset, end = sentence_splitter.map_offsets(o_offset, o_end)
                    while (len(tmp_sentences[sentence_idx])<end):
                        tmp_sentences = sentence_splitter.merge_sentences(sentence_idx)
                        tmp_entities[sentence_idx] += tmp_entities[sentence_idx+1]
                        del tmp_entities[sentence_idx+1]
                        sentence_idx, offset, end = sentence_splitter.map_offsets(o_offset, o_end)
                annotated_entity = tmp_sentences[sentence_idx][offset:end]
                true_entity = annotation.xpath('.//text')[0].text
                assert annotated_entity == true_entity

                tmp_entities[sentence_idx] += [(offset, end)]

            document_ids += [document_id] * len(tmp_sentences)
            sentences += tmp_sentences
            entities += tmp_entities

    return sentences, entities, document_ids
