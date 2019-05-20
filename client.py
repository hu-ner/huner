import json
import sys
import subprocess
import argparse
import requests


def get_ip(name: str):
    info = subprocess.run(["docker", "inspect", name], stdout=subprocess.PIPE).stdout
    info = json.loads(info)
    return info[0]['NetworkSettings']['IPAddress']



def has_entity(sent):
    has_ent = False 
    for tok, tag in sent:
        if tag != "O":
            has_ent = True
    return has_ent

class HUNERTagger:
    def __init__(self, names=None):
        self.names = names or ["huner"]
        self.ips = [get_ip(name) for name in self.names]

    def merge_entities(self, results):
        new_results = []
        for sent in results:
            new_sent = []
            curr_ent = []
            curr_name = None
            for tok, tag in sent:
                if "/" in tag:
                    name, tag = tag.split("/")
                if tag[0] in {"B", "O"} and len(curr_ent) > 0:
                    new_sent.append([" ".join(curr_ent), curr_name])
                    curr_ent = []
                    curr_name = None

                if tag[0] in {"B", "I"}:
                    curr_ent.append(tok)
                    curr_name = name
                else:
                    new_sent.append([tok, tag])

            if len(curr_ent) > 0:
                new_sent.append([" ".join(curr_ent), curr_name])
            new_results.append(new_sent)

        return new_results

    def merge_names(self, results):
        merged = results[0]
        for sent in merged:
            for i, (tok, tag) in enumerate(sent):
                if tag[0] in {"B", "I"}:
                    sent[i][1] = self.names[0] + "/" + tag


        for result, name in zip(results[1:], self.names[1:]):
            for merged_sent, other_sent in zip(merged, result):
                in_ent = False
                ent_begin = None
                ent_end = None
                for i, (tok, tag) in enumerate(other_sent):
                    if tag.startswith("B"):
                        in_ent = True
                        ent_begin = i
                    elif tag in {"B", "O"}:
                        if in_ent:
                            ent_end = i
                            
                            if not has_entity(merged_sent[ent_begin:ent_end]):
                                for j, (_, tag) in enumerate(other_sent[ent_begin:ent_end]):
                                    merged_sent[j][1] = name + '/' + tag
                    
                    if tag == 'O':
                        in_ent = False

                if in_ent:
                    ent_end = i+1
                    
                    if not has_entity(merged_sent[ent_begin:ent_end]):
                        for j, (_, tag) in enumerate(other_sent[ent_begin:ent_end]):
                            merged_sent[j][1] = name + '/' + tag

                                
        return merged

    def tag(self, text, split_sentences=True, tokenize=True, merge_names=False, merge_entities=False):
        data = {'text': text, 'split_sentences': split_sentences, 'tokenize': tokenize}
        results = []
        for name, ip in zip(self.names, self.ips):
            response = requests.post(f"http://{ip}:5000/tag", json=data)
            results.append(response.json())
        if merge_names:
            results = self.merge_names(results)

        if merge_entities:
            results = self.merge_entities(results)
        return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--name", required=True)
    parser.add_argument("--assume_sentence_splitted", action='store_true')
    parser.add_argument("--assume_tokenized", action='store_true')
    parser.add_argument("--batchsize", type=int, default=256) 
    args = parser.parse_args()

    tagger = HUNERTagger(names=[args.name])
    split_sentences = not args.assume_sentence_splitted and not args.assume_tokenized

    with open(args.input) as f_in, open(args.output, 'w') as f_out:
        buff = []
        c = 0
        for line in f_in:
            if args.assume_tokenized:
                line = [line.split()]
            elif args.assume_sentence_splitted:
                line = [line]
            else:
                line = [line]
            c += 1
            buff += line
            if c % args.batchsize == 0:
                tagged_line = tagger.tag(buff, split_sentences=split_sentences, tokenize=not args.assume_tokenized)[0]
                for sentence in tagged_line:
                    for tok, tag in sentence:
                        f_out.write(f"{tok}\tPOS\t{tag}\n")
                    f_out.write("\n")
                buff = []
        if buff:
            tagged_line = tagger.tag(buff, split_sentences=split_sentences, tokenize=not args.assume_tokenized)[0]
            for sentence in tagged_line:
                for tok, tag in sentence:
                    f_out.write(f"{tok}\tPOS\t{tag}\n")
                f_out.write("\n")

