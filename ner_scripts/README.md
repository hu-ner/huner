# The Unified BioNER evaluation corpora

This collection of scripts obtains 35 BioNER corpora and converts them into the common IOB format with POS tags. The corpora are split into training, development and test set in the ratio 6:1:3.

The corpora cover five domains, which are:
+ Cell lines
+ Chemicals
+ Diseases
+ Genes/Proteins
+ Species

As some of the corpora contain multiple of these entity types, they appear in the output multiple times.

## Requirements
The scripts run on `python3` and require version 3.5 or newer. Install python requirments with `pip install -r requirments.txt`.

For syntactic analysis the scripts depend on Apache OpenNLP. Please download and install it following the instructions at <https://opennlp.apache.org/>.
Please download the following models and put them in a `models/` subdirectory of your OpenNLP installation.
```
en-pos-maxent.bin
en-sent.bin
en-token.bin
```

## Usage
To obtain the corpora run:
```
python3 download_files.py
```
Please ensure, that the process finishes without any errors. You'll be instructed to download the CDR corpus manually, as it is password protected.

To convert and split the corpora please run:
```
OPENNLP=path/to/opennlp ./convert_corpora.sh
```
Please be aware that this will take a couple of days, as the syntactic analysis of hugh corpora are computationally expensive.

If you are an experienced unix user and have a multi-core machine with at least 32GB of memory available, you can also use:
```
OPENNLP=path/to/opennlp ./convert_corpora_parallel.sh
```
This will run all conversions in parallel, reducing the runtime to less than a day. Please be aware that due to concurrency issues, some conversion tasks may fail. Those have to be restarted manually, together with the downstream processing.
