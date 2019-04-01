# The HUNER tagger

This repository provides the HUNER tagger, an easy to use tagger for biomedical named entities. HUNER is able to annotate five different entity types:
+ Cell Lines
+ Chemicals
+ Diseases
+ Genes/Proteins
+ Species

## Requirements

HUNER is provided as a Docker container. Please install Docker following the instructions on the official webpage: <https://docs.docker.com/install/>

## Usage

To use HUNER please follow these steps:

1. Clone the repository
2. Download and unpack the necessary model files into the `models` folder. Model files are provided at <https://drive.google.com/open?id=1Y6vdSymGN5QEeEITPF2zZj4qUcoDWvXf>.
3. Start the server using `./start_server <model_name>`. Depending on your Docker installation, `sudo` rights might be required.
4. Tag your text using `python client.py INPUT.TXT OUTPUT.CONLL --name <model_name>`

If your text is already sentence split, use the `--assume_sentence_splitted` flag in the client. HUNER expects one sentence per line. If your text is in addition also already tokenized, use `--assume_tokenized`. Tokens are separated by a whitespace character.

Please be aware that HUNER assumes no newlines occur within sentences, irrespective of the flags.

The HUNER server exposes a JSON API over HTTP, with a single `/tag` method. Please consult `tagger.py` for details on the API.  We want to point out, that the HUNER server is not thread safe and might give invalid results for concurrent requests.

## The HUNER Corpora
For details and instructions on the HUNER corpora please refer to <https://github.com/hu-ner/huner/tree/master/ner_scripts> and the corresponding readme.
