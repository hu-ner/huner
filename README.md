# HUNER

*We recently published [HunFlair](https://github.com/flairNLP/flair/blob/master/resources/docs/HUNFLAIR.md), a reimplementation of HUNER inside the Flair framework. By using language models, HunFlair considerably outperforms HUNER. In addition, as part of Flair, HunFlair is easy to install and does not have a dependency on Docker. We recommend all HUNER users to migrate to HunFlair.*

HUNER is a state-of-the-art NER model for biomedical entities. It comes with models for genes/proteins, chemicals, diseases, species and cell lines.

The code is based on the great LSTM-CRF NER tagger implementation [glample/tagger](https://github.com/glample/tagger) by Guillaume Lample.

## Content
| Section | Description |
|-|-|
| [Installation](#installation) | How to install HUNER |
| [Usage](#usage) | How to use HUNER |
| [Models](#models) | Available pretrained models |
| [Corpora](#corpora) | The HUNER Corpora |


# Installation
1. [Install docker](https://docs.docker.com/install/)
1. Clone this repository to `$dir`
1. Download the pretrained model you want to use from [here](https://drive.google.com/drive/folders/1Y6vdSymGN5QEeEITPF2zZj4qUcoDWvXf), place it into `$dir/models/$model_name` and untar it using `tar xzf $model_name`

# Usage

# Tagging
To tokenize, sentence split and tag a file INPUT.TXT:

1. Start the HUNER server from `$dir` using `./start_server $model_name`. The model must reside in the directory `$dir/models/$model_name`.
1. Tag text with `python client.py INPUT.TXT OUTPUT.CONLL --name $model_name`.

the output will then be written to OUTPUT.CONLL in the conll2003 format.


The options for `client.py` are:
* `--asume_tokenized`: The input is already pre-tokenized and the tokens are separated by whitespace
* `--assume_sentence_splitted`: The input is already split into sentences and each line of the input contains one sentence

## Fine-tuning on a new corpus
The steps to fine-tune a base-model `$base_model` (e.g. `gene_all`) on a new corpus `$corpus` are:


1. Copy the chosen base-model to a new directory, because the weight files will be updated during fine-tuning:
```bash
cp $dir/models/$base_model $dir/models/$fine_tuned_model
```
2. Convert your corpus to conll format and split it into `train`, `dev` and `test` portions. If you don't want to use either dev or test data you can just provide the training data as `dev` or `test`. Note however, that without dev data, results will probably suffer, because early-stopping can't be performed.
3. Fine-tune the model:
```bash
./train.sh $fine_tuned_model $corpus_train $corpus_dev $corpus_test
```
After successful training, `$fine_tuned_model` will contain the fine-tuned model and can be used exactly like the models provided by us.

## Retraining a base-model from scratch (without fine-tuning)
To train a model from scratch without initializing it from a base-model, proceed as follows:
1. Convert your corpus to conll format and split it into `train`, `dev` and `test` portions. If you don't want to use either dev or test data you can just provide the training data as `dev` or `test`. Note however, that without dev data, results will probably suffer, because early-stopping can't be performed.
2. Train the model:
```bash
./train_no_finetune.sh $corpus_train $corpus_dev $corpus_test
```
After sucessful training, the model can be found in a newly created directory in `models/`. The directory name reflects the chosen hyper-parameters and usually reads like `tag_scheme=iob,lower=False,zeros=False,char_dim=25...`.



# Models
| Model | Test sets P / R / F1 (%) | CRAFT P / R / F1 (%) |
|   -   |       -      |    -     |
| [cellline_all](https://drive.google.com/open?id=1aqtenziAHmxEHeaHf8JGdTkRe21ovjts) | 70.40 / 65.37 / 67.76 | - |
| [chemical_all](https://drive.google.com/open?id=1lEXPKiMZ0x3y51epBIS2kWHG3cNxnN4r) | 83.34 / 80.26 / 81.71 | 53.56 / 35.85 / 42.95 |
| [disease_all](https://drive.google.com/open?id=12vdtSi3hg_htCXXROKkPV4jaDO3ep8OY) | 75.01 / 77.71 / 76.20 | - |
| [gene_all](https://drive.google.com/open?id=1xdMkeA5HynmrAe4Ky2QwJAqCjP3pp2EO) | 72.33 / 76.28 / 73.97 | 59.67 / 65.98 / 62.66 |
| [species_all](https://drive.google.com/open?id=1JO6JuG2gz7W3C_44dJ0gmCozKKFsAEo6) | 77.88 / 74.86 / 73.33 | 98.51 / 73.83 / 84.40 |

# Corpora
For details and instructions on the HUNER corpora please refer to https://github.com/hu-ner/huner/tree/master/ner_scripts and the corresponding readme.

# Citation
Please use the following bibtex entry:
```
@article{weber2019huner,
  title={HUNER: Improving Biomedical NER with Pretraining},
  author={Weber, Leon and M{\"u}nchmeyer, Jannes and Rockt{\"a}schel, Tim and Habibi, Maryam and Leser, Ulf},
  journal={Bioinformatics},
  year={2019}
}
```
