import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("splits")
args = parser.parse_args()


def write_file(f_out, sentences):
    for sentence in sentences:
        for line in sentence.split('\n'):
            f_out.write(' '.join(line.split()[1:]))
            f_out.write('\n')
        f_out.write('\n')

train_ids = set()
test_ids = set()
dev_ids = set()

with open(args.splits + '.train', 'r') as f_in:
    for line in f_in:
        train_ids.add(line.strip())

with open(args.splits + '.test', 'r') as f_in:
    for line in f_in:
        test_ids.add(line.strip())

with open(args.splits + '.dev', 'r') as f_in:
    for line in f_in:
        dev_ids.add(line.strip())

train_ids = sorted(train_ids)
test_ids = sorted(test_ids)
dev_ids = sorted(dev_ids)

with open(args.file, 'r') as f_in:
    text = f_in.read()
    sentences = [x.strip() for x in text.split('\n\n') if x.split()]
    sentences_per_doc = defaultdict(list)
    for sentence in sentences:
        doc_id = sentence.split()[0]
        sentences_per_doc[doc_id].append(sentence)

    train = []
    test = []
    dev = []

    for doc_id in train_ids:
        if len(sentences_per_doc[doc_id]) > 0:
            train += ["0 -DOCSTART- X X O"] # add dummy id as first column will be removed
            train += sentences_per_doc[doc_id]

    for doc_id in test_ids:
        if len(sentences_per_doc[doc_id]) > 0:
            test += ["0 -DOCSTART- X X O"]
            test += sentences_per_doc[doc_id]

    for doc_id in dev_ids:
        if len(sentences_per_doc[doc_id]) > 0:
            dev += ["0 -DOCSTART- X X O"]
            dev += sentences_per_doc[doc_id]

    with open(args.file+'.train', 'w') as f_out:
        write_file(f_out, train)
    with open(args.file+'.dev', 'w') as f_out:
        write_file(f_out, dev)
    with open(args.file+'.test', 'w') as f_out:
        write_file(f_out, test)
