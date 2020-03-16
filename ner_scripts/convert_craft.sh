#!/bin/sh

# Craft corpus can be obtained from http://sourceforge.net/projects/bionlp-corpora/files/CRAFT/v2.0/craft-2.0.tar.gz/download

CRAFT_DIR=$1

python scripts/craft_to_conll.py $CRAFT_DIR chebi craft_chemicals_tmp.conll
awk '{print (NF ? $2"\t"$3"\t"$4 : $0)}' craft_chemicals_tmp.conll > craft_chemicals.conll
rm craft_chemicals_tmp.conll

python scripts/craft_to_conll.py $CRAFT_DIR entrezgene,pr craft_genes_tmp.conll
awk '{print (NF ? $2"\t"$3"\t"$4 : $0)}' craft_genes_tmp.conll > craft_genes.conll
rm craft_genes_tmp.conll

python scripts/craft_to_conll.py $CRAFT_DIR ncbitaxon craft_species_tmp.conll
awk '{print (NF ? $2"\t"$3"\t"$4 : $0)}' craft_species_tmp.conll > craft_species.conll
rm craft_species_tmp.conll
