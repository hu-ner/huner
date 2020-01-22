#!/usr/bin/env python3
from glob import glob
import gzip
import os
import shutil
import tarfile
import zipfile
import requests
import rarfile
import shlex
import subprocess

if __name__ == '__main__':
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(parent_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)


    def file_exists(fname):
        return os.path.isfile(os.path.join(data_dir, fname))


    def is_missing(fnames):
        for fname in fnames:
            if not file_exists(fname):
                print(fname + " is missing. Downloading...")
                return True
        return False


    def is_empty(dirname):
        dirpath = os.path.join(data_dir, dirname)
        empty = (not os.path.isdir(dirpath)) or len(os.listdir(dirpath)) == 0
        if empty:
            print(dirname + " is missing. Downloading...")
            return True
        else:
            return False


    # Arizona
    # if not file_exists('arizona.txt'):
    #     ("http://diego.asu.edu/downloads/AZDC_6-26-2009.txt",
    #                 filename=os.path.join(data_dir, "arizona.txt"))


    # BioInfer
    if is_missing(['bioinfer.xml']):
        with open('bioinfer.zip', 'wb') as f:
            resp = requests.get('http://mars.cs.utu.fi/BioInfer/files/BioInfer_corpus_1.1.1.zip')
            f.write(resp.content)

        with zipfile.ZipFile('bioinfer.zip') as f:
            f.extractall()

        shutil.move('BioInfer_corpus_1.1.1.xml', os.path.join(data_dir, 'bioinfer.xml'))
        os.remove('bioinfer.zip')

    # Biosemantics
    if is_empty("biosemantics"):
        with open('Patent_Corpus.rar', 'wb') as f:
            resp = requests.get('http://biosemantics.org/PatentCorpus/Patent_Corpus.rar')
            f.write(resp.content)
        
        with rarfile.RarFile("Patent_Corpus.rar") as f:
            f.extractall()
            shutil.move(os.path.join("Patent_Corpus/Full_set"), os.path.join("data", "biosemantics"))
            os.remove("Patent_Corpus.rar")
            shutil.rmtree("Patent_Corpus")

    # CellFinder
    if is_empty('cellfinder'):
        with open('cellfinder.tar.gz', 'wb') as f:
            resp = requests.get("https://www.informatik.hu-berlin.de/de/forschung/gebiete/wbi/resources/cellfinder/cellfinder1_brat.tar.gz")
            f.write(resp.content)

        path = os.path.join(data_dir, 'cellfinder')
        os.makedirs(path)
        with tarfile.open("cellfinder.tar.gz") as f:
            f.extractall(path)
        os.remove("cellfinder.tar.gz")

    # CHEMDNER Patents
    if is_missing(['cemp_train.txt', 'cemp_train.ann',
                   'cemp_val.txt', 'cemp_val.ann']):
        with open('cemp_train.tar.gz', 'wb') as fp:
            resp = requests.get('https://biocreative.bioinformatics.udel.edu/media/store/files/2015/cemp_training_set.tar.gz')
            fp.write(resp.content)
        with open('cemp_val.tar.gz', 'wb') as fp:
            resp = requests.get('https://biocreative.bioinformatics.udel.edu/media/store/files/2015/cemp_development_set_v03.tar.gz')
            fp.write(resp.content)

        with tarfile.open('cemp_train.tar.gz') as f:
            f.extractall()
        os.remove('cemp_train.tar.gz')

        with tarfile.open('cemp_val.tar.gz') as f:
            f.extractall()
        os.remove('cemp_val.tar.gz')

        shutil.move(os.path.join('cemp_training_set', 'chemdner_patents_train_text.txt'),
                    os.path.join(data_dir, 'cemp_train.txt'))
        shutil.move(os.path.join('cemp_training_set', 'chemdner_cemp_gold_standard_train.tsv'),
                    os.path.join(data_dir, 'cemp_train.ann'))

        shutil.move(os.path.join('cemp_development_set_v03', 'chemdner_patents_development_text.txt'),
                    os.path.join(data_dir, 'cemp_val.txt'))
        shutil.move(os.path.join('cemp_development_set_v03', 'chemdner_cemp_gold_standard_development_v03.tsv'),
                    os.path.join(data_dir, 'cemp_val.ann'))

        shutil.rmtree('cemp_training_set')
        shutil.rmtree('cemp_development_set_v03')

    # CHEBI
    if is_empty('chebi'):
        cmd = 'cvs -z3 -d:pserver:anonymous@a.cvs.sourceforge.net:/cvsroot/chebi co -P chapati'
        cmd = shlex.split(cmd)
        subprocess.run(cmd)
        with tarfile.open(os.path.join('chapati', 'patentsGoldStandard', 'PatentAnnotations_GoldStandard.tgz')) as f:
            f.extractall()
            shutil.move('scrapbook', os.path.join(data_dir, 'chebi'))
        shutil.rmtree('chapati')


    # CHEMDNER
    if is_missing(['chemdner_train.txt', 'chemdner_train.ann',
                   'chemdner_val.txt', 'chemdner_val.ann',
                   'chemdner_test.txt', 'chemdner_test.ann'
                   ]):

        with open('chemdner.tar.gz', 'wb') as fp:
            resp = requests.get('https://biocreative.bioinformatics.udel.edu/media/store/files/2014/chemdner_corpus.tar.gz')
            fp.write(resp.content)

        with tarfile.open('chemdner.tar.gz') as f:
            f.extractall()
        shutil.move(os.path.join('chemdner_corpus', 'training.abstracts.txt'),
                    os.path.join(data_dir, 'chemdner_train.txt'))
        shutil.move(os.path.join('chemdner_corpus', 'training.annotations.txt'),
                    os.path.join(data_dir, 'chemdner_train.ann'))
        shutil.move(os.path.join('chemdner_corpus', 'development.abstracts.txt'),
                    os.path.join(data_dir, 'chemdner_val.txt'))
        shutil.move(os.path.join('chemdner_corpus', 'development.annotations.txt'),
                    os.path.join(data_dir, 'chemdner_val.ann'))
        shutil.move(os.path.join('chemdner_corpus', 'evaluation.abstracts.txt'),
                    os.path.join(data_dir, 'chemdner_test.txt'))
        shutil.move(os.path.join('chemdner_corpus', 'evaluation.annotations.txt'),
                    os.path.join(data_dir, 'chemdner_test.ann'))
        shutil.rmtree('chemdner_corpus')
        os.remove('chemdner.tar.gz')

    # # CLL
    # if is_empty('cll'):
    #     with open('cll.tar.gz', 'wb') as fp:
    #         resp = requests.get('http://bionlp-www.utu.fi/cell-lines/CLL_corpus.tar.gz')
    #         fp.write(resp.content)

    #     with tarfile.open('cll.tar.gz') as f:
    #         f.extractall()
    #     shutil.move(os.path.join('CLL_corpus', 'conll'),
    #                 os.path.join(data_dir, 'cll'))
    #     os.remove('cll.tar.gz')
    #     shutil.rmtree('CLL_corpus')

    # Gellus
    if is_empty('gellus'):
        with open('gellus.tar.gz', 'wb') as fp:
            resp = requests.get('http://bionlp-www.utu.fi/cell-lines/Gellus_corpus.tar.gz')
            fp.write(resp.content)

        with tarfile.open('gellus.tar.gz') as f:
            f.extractall()
        shutil.move(os.path.join(parent_dir,'GELLUS-1.0.3','conll','all'),
                    os.path.join(data_dir, 'gellus'))
        os.remove('gellus.tar.gz')
        shutil.rmtree('GELLUS-1.0.3')

    # DECA
    if is_empty('deca'):
        with open('deca.tar.gz', 'wb') as fp:
            resp = requests.get('http://www.nactem.ac.uk/deca/species_corpus_0.2.tar.gz')
            fp.write(resp.content)

        with tarfile.open('deca.tar.gz') as f:
            f.extractall()
        shutil.move('species_corpus_0.2', os.path.join(data_dir, 'deca'))
        os.remove('deca.tar.gz')

    # FSU-PRGE
    if is_empty('fsu'):
        with open('fsu.tar.gz', 'wb') as fp:
            resp = requests.get('https://julielab.de/downloads/resources/fsu_prge_release_v1_0.tgz')
            fp.write(resp.content)

        with tarfile.open('fsu.tar.gz') as f:
            f.extractall()
        shutil.move('fsu-prge-release-v1.0', os.path.join(data_dir, 'fsu'))
        os.remove('fsu.tar.gz')

    # GPRO
    if is_empty('gpro'):
        with open('gpro_train.tar.gz', 'wb') as fp:
            resp = requests.get('https://biocreative.bioinformatics.udel.edu/media/store/files/2015/gpro_training_set_v02.tar.gz')
            fp.write(resp.content)

        with open('gpro_val.tar.gz', 'wb') as fp:
            resp = requests.get('https://biocreative.bioinformatics.udel.edu/media/store/files/2015/gpro_development_set.tar_.gz')
            fp.write(resp.content)

        with tarfile.open('gpro_train.tar.gz') as f:
            f.extractall()

        with tarfile.open('gpro_val.tar.gz') as f:
            f.extractall()

        corpus_dir = os.path.join(data_dir, 'gpro')
        os.makedirs(corpus_dir, exist_ok=True)

        for fname in glob(os.path.join('gpro_training_set_v02', '*')) + glob(os.path.join('gpro_development_set', '*')):
            shutil.move(fname,corpus_dir)

        os.remove('gpro_train.tar.gz')
        os.remove('gpro_val.tar.gz')
        shutil.rmtree('gpro_training_set_v02')
        shutil.rmtree('gpro_development_set')

    # IEPA
    if is_missing(['iepa.xml']):
        with open('iepa.zip', 'wb') as fp:
        	resp = requests.get('http://corpora.informatik.hu-berlin.de/corpora/brat2bioc/iepa_bioc.xml.zip')
        	fp.write(resp.content)
        with zipfile.ZipFile('iepa.zip') as f:
            f.extractall()
        shutil.move('iepa_bioc.xml', os.path.join(data_dir, 'iepa.xml'))
        os.remove('iepa.zip')

    # JNLPBA
    if is_empty('jnlpba'):
        with open('genia_train.tar.gz', 'wb') as fp:
        	resp = requests.get('http://www.nactem.ac.uk/GENIA/current/Shared-tasks/JNLPBA/Train/Genia4ERtraining.tar.gz')
        	fp.write(resp.content)
        with open('genia_test.tar.gz', 'wb') as fp:
        	resp = requests.get('http://www.nactem.ac.uk/GENIA/current/Shared-tasks/JNLPBA/Evaluation/Genia4ERtest.tar.gz')
        	fp.write(resp.content)
        with tarfile.open('genia_train.tar.gz') as f:
            f.extractall(os.path.join(data_dir, 'jnlpba'))
        with tarfile.open('genia_test.tar.gz') as f:
            f.extractall(os.path.join(data_dir, 'jnlpba'))
        os.remove('genia_train.tar.gz')
        os.remove('genia_test.tar.gz')

    # Linneaus
    if is_empty('linneaus'):
        with open('linneaus.tar.gz', 'wb') as fp:
        	resp = requests.get('https://sourceforge.net/projects/linnaeus/files/Corpora/manual-corpus-species-1.0.tar.gz/download')
        	fp.write(resp.content)
        with tarfile.open('linneaus.tar.gz') as f:
            f.extractall()
        shutil.move('manual-corpus-species-1.0',
                    os.path.join(data_dir, 'linneaus'))
        os.remove('linneaus.tar.gz')

    # LocText
    if is_empty('loctext'):
        with open('loctext.tar.gz', 'wb') as fp:
        	resp = requests.get('https://www.tagtog.net/jmcejuela/LocText/-downloads/dataset-as-anndoc')
        	fp.write(resp.content)
        with tarfile.open('loctext.tar.gz') as f:
            f.extractall()
        shutil.move('LocText', os.path.join(data_dir, 'loctext'))
        os.remove('loctext.tar.gz')

    # miRNA
    if is_missing(['miRNA_test.xml', 'miRNA_train.xml']):
        with open(os.path.join(data_dir, 'miRNA_test.xml'), 'wb') as fp:
        	resp = requests.get('https://www.scai.fraunhofer.de/content/dam/scai/de/downloads/bioinformatik/miRNA/miRNA-Test-Corpus.xml')
        	fp.write(resp.content)
        with open(os.path.join(data_dir, 'miRNA_train.xml'), 'wb') as fp:
        	resp = requests.get('https://www.scai.fraunhofer.de/content/dam/scai/de/downloads/bioinformatik/miRNA/miRNA-Train-Corpus.xml')
        	fp.write(resp.content)

    # NCBI
    if is_empty('ncbi'):
        with open('ncbi_train.zip', 'wb') as fp:
        	resp = requests.get('https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/NCBItrainset_corpus.zip')
        	fp.write(resp.content)
        with open('ncbi_val.zip', 'wb') as fp:
        	resp = requests.get('https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/NCBIdevelopset_corpus.zip')
        	fp.write(resp.content)
        with open('ncbi_test.zip', 'wb') as fp:
        	resp = requests.get('https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/NCBItestset_corpus.zip')
        	fp.write(resp.content)
        with zipfile.ZipFile('ncbi_train.zip') as f:
            f.extractall(os.path.join(data_dir, 'ncbi'))
        with zipfile.ZipFile('ncbi_val.zip') as f:
            f.extractall(os.path.join(data_dir, 'ncbi'))
        with zipfile.ZipFile('ncbi_test.zip') as f:
            f.extractall(os.path.join(data_dir, 'ncbi'))
        os.remove('ncbi_train.zip')
        os.remove('ncbi_val.zip')
        os.remove('ncbi_test.zip')

    # Osiris
    if is_empty('osiris'):
        with open('osiris.tar', 'wb') as fp:
        	resp = requests.get('http://ibi.imim.es/OSIRIScorpusv02.tar')
        	fp.write(resp.content)
        with tarfile.open('osiris.tar') as f:
            f.extractall()
        shutil.move('OSIRIScorpusv02',
                    os.path.join(data_dir, 'osiris'))
        os.remove('osiris.tar')

    # S800
    if is_empty('s800'):
        with open('s800.tar.gz', 'wb') as fp:
        	resp = requests.get('https://species.jensenlab.org/files/S800-1.0.tar.gz')
        	fp.write(resp.content)
        with tarfile.open('s800.tar.gz') as f:
            f.extractall(os.path.join(data_dir, 's800'))
        os.remove('s800.tar.gz')

    # SCAI Chemicals
    if is_missing(['scai_chemicals.conll']):
        with open('scai_chemicals.gz', 'wb') as fp:
        	resp = requests.get('https://www.scai.fraunhofer.de/content/dam/scai/de/downloads/bioinformatik/Corpora-for-Chemical-Entity-Recognition/chemicals-test-corpus-27-04-2009-v3_iob.gz')
        	fp.write(resp.content)
        with gzip.open('scai_chemicals.gz') as f_in, open(os.path.join(data_dir, 'scai_chemicals.conll'), 'wb') as f_out:
            f_out.write(f_in.read())
        os.remove('scai_chemicals.gz')

    # SCAI Diseases
    if is_missing(['scai_diseases.conll']):
        with open(os.path.join(data_dir, 'scai_diseases.conll'), 'wb') as fp:
        	resp = requests.get('https://www.scai.fraunhofer.de/content/dam/scai/de/downloads/bioinformatik/Disease-ae-corpus.iob')
        	fp.write(resp.content)

    # Variome
    if is_missing(['variome.xml']):
        with open('variome.zip', 'wb') as fp:
        	resp = requests.get('http://corpora.informatik.hu-berlin.de/corpora/brat2bioc/hvp_bioc.xml.zip')
        	fp.write(resp.content)
        with zipfile.ZipFile('variome.zip') as f:
            f.extractall()
        shutil.move('hvp_bioc.xml', os.path.join(data_dir, 'variome.xml'))
        os.remove('variome.zip')

    # CDR
    if is_empty('CDR_Data'):
        raise ValueError("Please download the data from https://biocreative.bioinformatics.udel.edu/tasks/biocreative-v/track-3-cdr/ and move the extracted directory to data/ ...")

    # Biocreative
    if is_empty('bc2gm/train') or is_empty('bc2gm/test'):
        raise ValueError("Please download the train and test data for the GM subtask from https://biocreative.bioinformatics.udel.edu/resources/corpora/biocreative-ii-corpus/ and place the directories named 'train' and 'test' into data/bc2gm ...")


    print("Success! All corpora should now be available.")
