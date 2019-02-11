#!/bin/sh

if [ -z "$1" ] 
then
    base_dir="."
else
    base_dir="$1"
fi

DISEASE_DIR="$base_dir"/converted/disease
GENE_DIR="$base_dir"/converted/gene
SPECIES_DIR="$base_dir"/converted/species
CELLLINE_DIR="$base_dir"/converted/cellline
CHEMICAL_DIR="$base_dir"/converted/chemical
SPLIT_DIR=splits
SCRIPT_DIR=scripts

python3 $SCRIPT_DIR/split_corpora.py $GENE_DIR/osiris.conll $SPLIT_DIR/osiris
python3 $SCRIPT_DIR/split_corpora.py $GENE_DIR/bc2gm.conll $SPLIT_DIR/bc2gm
python3 $SCRIPT_DIR/split_corpora.py $GENE_DIR/bioinfer.conll $SPLIT_DIR/bioinfer
python3 $SCRIPT_DIR/split_corpora.py $GENE_DIR/loctext.conll $SPLIT_DIR/loctext
python3 $SCRIPT_DIR/split_corpora.py $GENE_DIR/cellfinder.conll $SPLIT_DIR/cellfinder_protein
python3 $SCRIPT_DIR/split_corpora.py $GENE_DIR/variome.conll $SPLIT_DIR/variome_gene
python3 $SCRIPT_DIR/split_corpora.py $GENE_DIR/iepa.conll $SPLIT_DIR/iepa
python3 $SCRIPT_DIR/split_corpora.py $GENE_DIR/jnlpba.conll $SPLIT_DIR/genia
python3 $SCRIPT_DIR/split_corpora.py $GENE_DIR/deca.conll $SPLIT_DIR/deca
python3 $SCRIPT_DIR/split_corpora.py $GENE_DIR/fsu.conll $SPLIT_DIR/fsu
python3 $SCRIPT_DIR/split_corpora.py $GENE_DIR/gpro.conll $SPLIT_DIR/gpro
python3 $SCRIPT_DIR/split_corpora.py $GENE_DIR/miRNA.conll $SPLIT_DIR/miRNA
python3 $SCRIPT_DIR/split_corpora.py $DISEASE_DIR/scai_diseases.conll $SPLIT_DIR/scai_disease
python3 $SCRIPT_DIR/split_corpora.py $DISEASE_DIR/ncbi.conll $SPLIT_DIR/ncbi
python3 $SCRIPT_DIR/split_corpora.py $DISEASE_DIR/cdr.conll $SPLIT_DIR/CDRDisease
python3 $SCRIPT_DIR/split_corpora.py $DISEASE_DIR/biosemantics.conll $SPLIT_DIR/bios
python3 $SCRIPT_DIR/split_corpora.py $DISEASE_DIR/variome.conll $SPLIT_DIR/variome_disease
# python3 $SCRIPT_DIR/split_corpora.py $DISEASE_DIR/arizona.conll $SPLIT_DIR/arizona
python3 $SCRIPT_DIR/split_corpora.py $DISEASE_DIR/miRNA.conll $SPLIT_DIR/miRNA
python3 $SCRIPT_DIR/split_corpora.py $CELLLINE_DIR/cellfinder.conll $SPLIT_DIR/cellfinder_cellline
python3 $SCRIPT_DIR/split_corpora.py $CELLLINE_DIR/cll.conll $SPLIT_DIR/cll
python3 $SCRIPT_DIR/split_corpora.py $CELLLINE_DIR/gellus.conll $SPLIT_DIR/gellus
python3 $SCRIPT_DIR/split_corpora.py $CELLLINE_DIR/jnlpba.conll $SPLIT_DIR/genia
python3 $SCRIPT_DIR/split_corpora.py $SPECIES_DIR/cellfinder.conll $SPLIT_DIR/cellfinder_species
python3 $SCRIPT_DIR/split_corpora.py $SPECIES_DIR/variome.conll $SPLIT_DIR/variome_species
python3 $SCRIPT_DIR/split_corpora.py $SPECIES_DIR/s800.conll $SPLIT_DIR/s800
python3 $SCRIPT_DIR/split_corpora.py $SPECIES_DIR/linneaus.conll $SPLIT_DIR/linneaus
python3 $SCRIPT_DIR/split_corpora.py $SPECIES_DIR/loctext.conll $SPLIT_DIR/loctext
python3 $SCRIPT_DIR/split_corpora.py $SPECIES_DIR/miRNA.conll $SPLIT_DIR/miRNA
python3 $SCRIPT_DIR/split_corpora.py $CHEMICAL_DIR/cdr.conll $SPLIT_DIR/CDRChem
python3 $SCRIPT_DIR/split_corpora.py $CHEMICAL_DIR/cemp.conll $SPLIT_DIR/cemp
python3 $SCRIPT_DIR/split_corpora.py $CHEMICAL_DIR/chebi.conll $SPLIT_DIR/chebi
python3 $SCRIPT_DIR/split_corpora.py $CHEMICAL_DIR/chemdner.conll $SPLIT_DIR/chemdner
python3 $SCRIPT_DIR/split_corpora.py $CHEMICAL_DIR/biosemantics.conll $SPLIT_DIR/bios
python3 $SCRIPT_DIR/split_corpora.py $CHEMICAL_DIR/scai_chemicals.conll $SPLIT_DIR/scai_chemicals

