#!/usr/bin/env python3
from glob import glob
import gzip
import os
import shutil
import tarfile
import zipfile
from urllib.request import urlretrieve
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
    #     urlretrieve("http://diego.asu.edu/downloads/AZDC_6-26-2009.txt",
    #                 filename=os.path.join(data_dir, "arizona.txt"))


    # BioInfer
    if is_missing(['bioinfer.xml']):
        urlretrieve('http://mars.cs.utu.fi/BioInfer/files/BioInfer_corpus_1.1.1.zip',
                    'bioinfer.zip')

        with zipfile.ZipFile('bioinfer.zip') as f:
            f.extractall()

        shutil.move('BioInfer_corpus_1.1.1.xml', os.path.join(data_dir, 'bioinfer.xml'))
        os.remove('bioinfer.zip')

    # Biosemantics
    if is_empty("biosemantics"):
        urlretrieve("http://biosemantics.org/PatentCorpus/Patent_Corpus.rar",
                    "Patent_Corpus.rar")
        with rarfile.RarFile("Patent_Corpus.rar") as f:
            f.extractall()
            shutil.move(os.path.join("Patent_Corpus/Full_set"), os.path.join("data", "biosemantics"))
            os.remove("Patent_Corpus.rar")
            shutil.rmtree("Patent_Corpus")

    # CellFinder
    if is_empty('cellfinder'):
        urlretrieve(
            "https://www.informatik.hu-berlin.de/de/forschung/gebiete/wbi/resources/cellfinder/cellfinder1_brat.tar.gz",
            "cellfinder.tar.gz")
        path = os.path.join(data_dir, 'cellfinder')
        os.makedirs(path)
        with tarfile.open("cellfinder.tar.gz") as f:
            f.extractall(path)
        os.remove("cellfinder.tar.gz")

    # CHEMDNER Patents
    if is_missing(['cemp_train.txt', 'cemp_train.ann',
                   'cemp_val.txt', 'cemp_val.ann']):
        urlretrieve('http://www.biocreative.org/media/store/files/2015/cemp_training_set.tar.gz',
                    'cemp_train.tar.gz')
        urlretrieve('http://www.biocreative.org/media/store/files/2015/cemp_development_set_v03.tar.gz',
                    'cemp_val.tar.gz')

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
        urlretrieve('http://www.biocreative.org/media/store/files/2014/chemdner_corpus.tar.gz',
                    'chemdner.tar.gz')
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

    # CLL
    if is_empty('cll'):
        urlretrieve('http://bionlp-www.utu.fi/cell-lines/CLL_corpus.tar.gz',
                    'cll.tar.gz')
        with tarfile.open('cll.tar.gz') as f:
            f.extractall()
        shutil.move(os.path.join('CLL_corpus', 'conll'),
                    os.path.join(data_dir, 'cll'))
        os.remove('cll.tar.gz')
        shutil.rmtree('CLL_corpus')

    # Gellus
    if is_empty('gellus'):
        urlretrieve('http://bionlp-www.utu.fi/cell-lines/Gellus_corpus.tar.gz',
                    'gellus.tar.gz')
        with tarfile.open('gellus.tar.gz') as f:
            f.extractall()
        shutil.move(os.path.join('home','smp','cellline_data','GELLUS-1.0.3','conll','all'),
                    os.path.join(data_dir, 'gellus'))
        os.remove('gellus.tar.gz')
        shutil.rmtree('home')

    # DECA
    if is_empty('deca'):
        urlretrieve('http://www.nactem.ac.uk/deca/species_corpus_0.2.tar.gz',
                    'deca.tar.gz')
        with tarfile.open('deca.tar.gz') as f:
            f.extractall()
        shutil.move('species_corpus_0.2', os.path.join(data_dir, 'deca'))
        os.remove('deca.tar.gz')

    # FSU-PRGE
    if is_empty('fsu'):
        urlretrieve('https://julielab.de/downloads/resources/fsu_prge_release_v1_0.tgz',
                    'fsu.tar.gz')
        with tarfile.open('fsu.tar.gz') as f:
            f.extractall()
        shutil.move('fsu-prge-release-v1.0', os.path.join(data_dir, 'fsu'))
        os.remove('fsu.tar.gz')

    # GPRO
    if is_empty('gpro'):
        urlretrieve('http://www.biocreative.org/media/store/files/2015/gpro_training_set_v02.tar.gz',
                    'gpro_train.tar.gz')
        urlretrieve('http://www.biocreative.org/media/store/files/2015/gpro_development_set.tar_.gz',
                    'gpro_val.tar.gz')

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

    # IEPA
    if is_missing(['iepa.xml']):
        urlretrieve('http://corpora.informatik.hu-berlin.de/corpora/brat2bioc/iepa_bioc.xml.zip',
                    'iepa.zip')
        with zipfile.ZipFile('iepa.zip') as f:
            f.extractall()
        shutil.move('iepa_bioc.xml', os.path.join(data_dir, 'iepa.xml'))
        os.remove('iepa.zip')

    # JNLPBA
    if is_empty('jnlpba'):
        urlretrieve('http://www.nactem.ac.uk/tsujii/GENIA/ERtask/Genia4ERtraining.tar.gz',
                    'genia_train.tar.gz')
        urlretrieve('http://www.nactem.ac.uk/tsujii/GENIA/ERtask/Genia4ERtest.tar.gz',
                    'genia_test.tar.gz')
        with tarfile.open('genia_train.tar.gz') as f:
            f.extractall(os.path.join(data_dir, 'jnlpba'))
        with tarfile.open('genia_test.tar.gz') as f:
            f.extractall(os.path.join(data_dir, 'jnlpba'))
        os.remove('genia_train.tar.gz')
        os.remove('genia_test.tar.gz')

    # Linneaus
    if is_empty('linneaus'):
        urlretrieve('https://sourceforge.net/projects/linnaeus/files/Corpora/manual-corpus-species-1.0.tar.gz/download',
                    'linneaus.tar.gz')
        with tarfile.open('linneaus.tar.gz') as f:
            f.extractall()
        shutil.move('manual-corpus-species-1.0',
                    os.path.join(data_dir, 'linneaus'))
        os.remove('linneaus.tar.gz')

    # LocText
    if is_empty('loctext'):
        urlretrieve('https://www.tagtog.net/-corpora/-dl/loctext/pubannotation',
                    'loctext.tar.gz')
        with tarfile.open('loctext.tar.gz') as f:
            f.extractall()
        shutil.move('LocText', os.path.join(data_dir, 'loctext'))
        os.remove('loctext.tar.gz')

    # miRNA
    if is_missing(['miRNA_test.xml', 'miRNA_train.xml']):
        urlretrieve('https://www.scai.fraunhofer.de/content/dam/scai/de/downloads/bioinformatik/miRNA/miRNA-Test-Corpus.xml', os.path.join(data_dir, 'miRNA_test.xml'))
        urlretrieve('https://www.scai.fraunhofer.de/content/dam/scai/de/downloads/bioinformatik/miRNA/miRNA-Train-Corpus.xml', os.path.join(data_dir, 'miRNA_train.xml'))

    # NCBI
    if is_empty('ncbi'):
        urlretrieve('https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/NCBItrainset_corpus.zip',
                    'ncbi_train.zip')
        urlretrieve('https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/NCBIdevelopset_corpus.zip',
                    'ncbi_val.zip')
        urlretrieve('https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/NCBItestset_corpus.zip',
                    'ncbi_test.zip')
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
        urlretrieve('http://ibi.imim.es/OSIRIScorpusv02.tar', 'osiris.tar')
        with tarfile.open('osiris.tar') as f:
            f.extractall()
        shutil.move('OSIRIScorpusv02',
                    os.path.join(data_dir, 'osiris'))
        os.remove('osiris.tar')

    # S800
    if is_empty('s800'):
        urlretrieve('https://species.jensenlab.org/files/S800-1.0.tar.gz',
                    's800.tar.gz')
        with tarfile.open('s800.tar.gz') as f:
            f.extractall(os.path.join(data_dir, 's800'))
        os.remove('s800.tar.gz')

    # SCAI Chemicals
    if is_missing(['scai_chemicals.conll']):
        urlretrieve('https://www.scai.fraunhofer.de/content/dam/scai/de/downloads/bioinformatik/Corpora-for-Chemical-Entity-Recognition/chemicals-test-corpus-27-04-2009-v3_iob.gz',
                    'scai_chemicals.gz')
        with gzip.open('scai_chemicals.gz') as f_in, open(os.path.join(data_dir, 'scai_chemicals.conll'), 'wb') as f_out:
            f_out.write(f_in.read())
        os.remove('scai_chemicals.gz')

    # SCAI Diseases
    if is_missing(['scai_diseases.conll']):
        urlretrieve('https://www.scai.fraunhofer.de/content/dam/scai/de/downloads/bioinformatik/Disease-ae-corpus.iob',
                    os.path.join(data_dir, 'scai_diseases.conll'))

    # Variome
    if is_missing(['variome.xml']):
        urlretrieve('http://corpora.informatik.hu-berlin.de/corpora/brat2bioc/hvp_bioc.xml.zip',
                    'variome.zip')
        with zipfile.ZipFile('variome.zip') as f:
            f.extractall()
        shutil.move('hvp_bioc.xml', os.path.join(data_dir, 'variome.xml'))
        os.remove('variome.zip')

    # CDR
    if is_empty('CDR_Data'):
        raise ValueError("Please download the data from http://www.biocreative.org/tasks/biocreative-v/track-3-cdr/ and move the extracted directory to data/ ...")

    # Biocreative
    if is_empty('bc2gm/train') or is_empty('bc2gm/test'):
        raise ValueError("Please download the train and test data for the GM subtask from http://www.biocreative.org/resources/corpora/biocreative-ii-corpus/ and place the directories named 'train' and 'test' into data/bc2gm ...")


    print("Success! All corpora should now be available.")
