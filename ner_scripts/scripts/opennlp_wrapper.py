import pexpect
from subprocess import Popen, PIPE


class OpenNLP():
    def __init__(self, path, tool, model):
        '''
            Initializes OpenNLP
            :params
                path: Absolute path to the opennlp folder
                tool:OpenNLP tool (Eg: ChunkerME, TokenizerME)
                model: model file name
        '''
        opennlp = path + '/bin/opennlp'
        model_path = path + '/models/' + model
        cmd = '%s %s %s' % (opennlp, tool, model_path)

        # Spawn the chunker process
        self.process = pexpect.spawn(cmd)
        self.process.setecho(False)
        self.process.expect('done')
        self.process.expect('\r\n')

    def parse(self, text):
        # clear any pending output
        try:
            self.process.read_nonblocking(2048, 0)
        except:
            pass

        self.process.sendline(text)
        self.process.waitnoecho()  # remove this if not working
        timeout = 5 + len(text) / 20.0

        self.process.expect('\r\n', timeout)
        results = self.process.before
        if len(text) != 0:
            while len(results) == 0:
                self.process.expect('\r\n', timeout)
                results = self.process.before

        # Remove this if block if required.
        # This is added to address invalid input format for ChunkerME
        if b'Invalid' in results:
            try:
                self.process.readline()
            except:
                pass
            return False
        return results


class SentenceSplitter():
    def __init__(self, path, model):
        opennlp = path + '/bin/opennlp'
        model_path = path + '/models/' + model
        self.cmd = [opennlp, 'SentenceDetector', model_path]
        self.sentences = []
        self.sentence_offsets = []
        self.text = None

    def split(self, text):
        self.text = text
        p = Popen(self.cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        result, err = p.communicate(text.encode('utf-8'))
        result = result.decode('utf-8')
        self.sentences = result.split('\n')
        self.calc_offsets()
        return self.sentences

    def calc_offsets(self):
        self.sentence_offsets = []
        akt_pos = 0
        for sentence in self.sentences:
            if sentence:
                akt_pos = self.text.find(sentence[0], akt_pos)
                self.sentence_offsets += [akt_pos]
                akt_pos += len(sentence)
            else:
                self.sentence_offsets += [akt_pos]

    def map_offsets(self, start, end):
        minp = 0
        maxp = len(self.sentence_offsets)
        while (maxp-minp!=1):
            m = (maxp+minp)//2
            if self.sentence_offsets[m] > start:
                maxp = m
            else:
                minp = m
        sentence_id = minp
        new_start = start - self.sentence_offsets[minp]
        new_end = end - self.sentence_offsets[minp]
        return sentence_id, new_start, new_end

    def merge_sentences(self, id):
        # Merges sentences id and id+1
        spaces = self.sentence_offsets[id+1]-self.sentence_offsets[id]-len(self.sentences[id])
        self.sentences[id] += ' ' * spaces + self.sentences[id+1]
        del self.sentences[id+1]
        del self.sentence_offsets[id+1]
        return self.sentences
