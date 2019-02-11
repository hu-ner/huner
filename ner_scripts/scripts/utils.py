from itertools import combinations
from opennlp_wrapper import OpenNLP
import os
from tqdm import tqdm


def overlap(entity1, entity2):
    return range(max(entity1[0], entity2[0]), min(entity1[1], entity2[1]))


def merge_overlapping_entities(entities):
    entities = list(entities)

    entity_set_stable = False
    while not entity_set_stable:
        for e1, e2 in combinations(entities, 2):
            if overlap(e1, e2):
                merged_entity = (min(e1[0], e2[0]), max(e1[1], e2[1]))
                entities.remove(e1)
                entities.remove(e2)
                entities.append(merged_entity)
                break
        else:
            entity_set_stable = True

    return entities


def compute_token_char_offsets(tokens, sentence):
    start_idx = 0
    end_idx = 0

    indices = []
    for token in tokens:
        start_idx = end_idx
        while not sentence[start_idx].strip():
            start_idx += 1
        end_idx = start_idx + len(token)

        #if token != sentence[start_idx:end_idx]:
        #    import IPython;IPython.embed()

        assert token == sentence[start_idx:end_idx]

        indices.append((start_idx, end_idx))

    return indices


def write_to_conll(sentences, entities_per_sentence, document_ids,
                   output_file, tokenizer=None):
    opennlp_path = os.environ['OPENNLP']
    if tokenizer is None:
        opennlp_tokenizer = OpenNLP(opennlp_path, 'TokenizerME', 'en-token.bin')
        def tokenizer(sentence):
            return opennlp_tokenizer.parse(sentence).decode().split()

    pos_tagger = OpenNLP(opennlp_path, 'POSTagger', 'en-pos-maxent.bin')

    for sentence, entities, document_id in tqdm(list(zip(sentences, entities_per_sentence, document_ids))):
        if len(sentence) == 0:
            continue

        tokens = [token for token in tokenizer(sentence)]
        entities = [range(*e) for e in entities]
        in_entity = False

        token_char_offsets = compute_token_char_offsets([token for token in tokens], sentence)
        pos_tags = pos_tagger.parse(' '.join(tokens)).decode()

        for (start_idx, end_idx), token_pos in zip(token_char_offsets, pos_tags.split()):
            token = '_'.join(token_pos.split('_')[:-1])
            pos_tag = token_pos.split('_')[-1]
            for entity in entities:
                if start_idx in entity:
                    if in_entity != entity:
                        tag = 'B-NP'
                        in_entity = entity
                    else:
                        tag = 'I-NP'
                    break
            else:
                tag = 'O'
                in_entity = False

            output_file.write(document_id+' '+token+' '+pos_tag+' '+tag+'\n')
        output_file.write('\n')
