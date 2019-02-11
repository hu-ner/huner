#!/bin/sh

DATA_DIR=data
DISEASE_DIR=converted/disease
GENE_DIR=converted/gene
SPECIES_DIR=converted/species
CELLLINE_DIR=converted/cellline
CHEMICAL_DIR=converted/chemical
PATCH_DIR=patches
SCRIPT_DIR=scripts

mkdir -p $DISEASE_DIR
mkdir -p $GENE_DIR
mkdir -p $SPECIES_DIR
mkdir -p $CELLLINE_DIR
mkdir -p $CHEMICAL_DIR

patch $DATA_DIR/CDR_Data/CDR_Data/CDR.Corpus.v010516/CDR_TrainingSet.BioC.xml patches/CDR_TrainingSet.BioC.xml.patch -o $DATA_DIR/CDR_Data/CDR_Data/CDR.Corpus.v010516/CDR_TrainingSet.BioC.xml.patched
patch $DATA_DIR/ncbi/NCBItrainset_corpus.txt $PATCH_DIR/NCBItrainset_corpus.patch -o $DATA_DIR/ncbi/NCBItrainset_corpus.txt.patched
patch $DATA_DIR/variome.xml $PATCH_DIR/variome.patch -o $DATA_DIR/variome.xml.patched

echo "Starting conversion processing"

# Arizona disease
python3 $SCRIPT_DIR/arizona_disease_to_conll.py $DATA_DIR/arizona.txt $DISEASE_DIR/arizona.conll &

# BioCreative 2 GeneMentions
python3 $SCRIPT_DIR/bc2gm_gene_to_conll.py $DATA_DIR/bc2gm/train/train.in $DATA_DIR/bc2gm/train/GENE.eval $GENE_DIR/bc2gm1.conll &
python3 $SCRIPT_DIR/bc2gm_gene_to_conll.py $DATA_DIR/bc2gm/test/test.in $DATA_DIR/bc2gm/test/GENE.eval $GENE_DIR/bc2gm2.conll &

# BioInfer
python3 $SCRIPT_DIR/bioinfer_to_conll.py $DATA_DIR/bioinfer.xml $GENE_DIR/bioinfer.conll &

# Biosemantics
python3 $SCRIPT_DIR/biosemantics_to_conll.py $DATA_DIR/biosemantics M,I,Y,D,B,C,F,R,G,MOA $CHEMICAL_DIR/biosemantics.conll &
python3 $SCRIPT_DIR/biosemantics_to_conll.py $DATA_DIR/biosemantics Disease $DISEASE_DIR/biosemantics.conll &

# CDR
python3 $SCRIPT_DIR/cdr_to_conll.py $DATA_DIR/CDR_Data/CDR_Data/CDR.Corpus.v010516/CDR_DevelopmentSet.BioC.xml $DISEASE_DIR/cdr1.conll Disease &
python3 $SCRIPT_DIR/cdr_to_conll.py $DATA_DIR/CDR_Data/CDR_Data/CDR.Corpus.v010516/CDR_DevelopmentSet.BioC.xml $CHEMICAL_DIR/cdr1.conll Chemical &
python3 $SCRIPT_DIR/cdr_to_conll.py $DATA_DIR/CDR_Data/CDR_Data/CDR.Corpus.v010516/CDR_TestSet.BioC.xml $DISEASE_DIR/cdr2.conll Disease &
python3 $SCRIPT_DIR/cdr_to_conll.py $DATA_DIR/CDR_Data/CDR_Data/CDR.Corpus.v010516/CDR_TestSet.BioC.xml $CHEMICAL_DIR/cdr2.conll Chemical &
python3 $SCRIPT_DIR/cdr_to_conll.py $DATA_DIR/CDR_Data/CDR_Data/CDR.Corpus.v010516/CDR_TrainingSet.BioC.xml.patched $DISEASE_DIR/cdr3.conll Disease &
python3 $SCRIPT_DIR/cdr_to_conll.py $DATA_DIR/CDR_Data/CDR_Data/CDR.Corpus.v010516/CDR_TrainingSet.BioC.xml.patched $CHEMICAL_DIR/cdr3.conll Chemical &

# CellFinder
python3 $SCRIPT_DIR/cellfinder_to_conll.py $DATA_DIR/cellfinder CellLine $CELLLINE_DIR/cellfinder.conll &
python3 $SCRIPT_DIR/cellfinder_to_conll.py $DATA_DIR/cellfinder Species $SPECIES_DIR/cellfinder.conll &
python3 $SCRIPT_DIR/cellfinder_to_conll.py $DATA_DIR/cellfinder GeneProtein $GENE_DIR/cellfinder.conll &

# CEMP
python3 $SCRIPT_DIR/gpro_gene_to_conll.py $DATA_DIR/cemp_train.txt $DATA_DIR/cemp_train.ann $CHEMICAL_DIR/cemp1.conll &
python3 $SCRIPT_DIR/gpro_gene_to_conll.py $DATA_DIR/cemp_val.txt $DATA_DIR/cemp_val.ann $CHEMICAL_DIR/cemp2.conll &

# CHEBI
python3 $SCRIPT_DIR/chebi_to_conll.py $DATA_DIR/chebi $CHEMICAL_DIR/chebi.conll &

# CHEMDNER
python3 $SCRIPT_DIR/gpro_gene_to_conll.py $DATA_DIR/chemdner_test.txt $DATA_DIR/chemdner_test.ann $CHEMICAL_DIR/chemdner1.conll &
python3 $SCRIPT_DIR/gpro_gene_to_conll.py $DATA_DIR/chemdner_train.txt $DATA_DIR/chemdner_train.ann $CHEMICAL_DIR/chemdner2.conll &
python3 $SCRIPT_DIR/gpro_gene_to_conll.py $DATA_DIR/chemdner_val.txt $DATA_DIR/chemdner_val.ann $CHEMICAL_DIR/chemdner3.conll &

# CLL
python3 $SCRIPT_DIR/cll_cell_lines_to_conll.py "$DATA_DIR/cll/*" $CELLLINE_DIR/cll.conll &

# DECA
python3 $SCRIPT_DIR/deca_genes_to_conll.py $DATA_DIR/deca $GENE_DIR/deca.conll &

# FSU
python3 $SCRIPT_DIR/fsu_gene_to_conll.py $DATA_DIR/fsu/Genes_cytorec,$DATA_DIR/fsu/Genes_genetag1,$DATA_DIR/fsu/Genes_genetag2,$DATA_DIR/fsu/Genes_LLL_Aimed,$DATA_DIR/fsu/Genes_PIR,$DATA_DIR/fsu/Genes_x45_shuffled,$DATA_DIR/fsu/Proteins_0,$DATA_DIR/fsu/Proteins0_shuffled,$DATA_DIR/fsu/Proteins_5,$DATA_DIR/fsu/Proteins_ecoli,$DATA_DIR/fsu/Proteins_KIR $GENE_DIR/fsu.conll &

# GELLUS
python3 $SCRIPT_DIR/gellus_to_conll.py "$DATA_DIR/gellus/*" $CELLLINE_DIR/gellus.conll &

# GPRO
python3 $SCRIPT_DIR/gpro_gene_to_conll.py $DATA_DIR/gpro/chemdner_patents_development_text.txt $DATA_DIR/gpro/chemdner_gpro_gold_standard_development.tsv $GENE_DIR/gpro1.conll &
python3 $SCRIPT_DIR/gpro_gene_to_conll.py $DATA_DIR/gpro/chemdner_patents_train_text.txt $DATA_DIR/gpro/chemdner_gpro_gold_standard_train_v02.tsv $GENE_DIR/gpro2.conll &

# IEPA
python3 $SCRIPT_DIR/iepa_gene_to_conll.py $DATA_DIR/iepa.xml $GENE_DIR/iepa.conll &

# JNLPBA
python3 $SCRIPT_DIR/jnlpba_to_conll.py $DATA_DIR/jnlpba/Genia4ERtask2.iob2 cell_line,cell_type $CELLLINE_DIR/jnlpba.conll &
python3 $SCRIPT_DIR/jnlpba_to_conll.py $DATA_DIR/jnlpba/Genia4ERtask2.iob2 protein $GENE_DIR/jnlpba.conll &

# Linneaus
python3 $SCRIPT_DIR/linneaus_species_to_conll.py $DATA_DIR/linneaus $SPECIES_DIR/linneaus.conll &

# Loctext
python3 $SCRIPT_DIR/loctext_gene_to_conll.py $DATA_DIR/loctext uniprot,go $GENE_DIR/loctext.conll &
python3 $SCRIPT_DIR/loctext_gene_to_conll.py $DATA_DIR/loctext taxonomy $SPECIES_DIR/loctext.conll &

# miRNA
python3 $SCRIPT_DIR/mirna_to_conll.py $DATA_DIR/miRNA_test.xml Genes/Proteins $GENE_DIR/miRNA1.conll &
python3 $SCRIPT_DIR/mirna_to_conll.py $DATA_DIR/miRNA_train.xml Genes/Proteins $GENE_DIR/miRNA2.conll &
python3 $SCRIPT_DIR/mirna_to_conll.py $DATA_DIR/miRNA_test.xml Species $SPECIES_DIR/miRNA1.conll &
python3 $SCRIPT_DIR/mirna_to_conll.py $DATA_DIR/miRNA_train.xml Species $SPECIES_DIR/miRNA2.conll &
python3 $SCRIPT_DIR/mirna_to_conll.py $DATA_DIR/miRNA_test.xml Diseases $DISEASE_DIR/miRNA1.conll &
python3 $SCRIPT_DIR/mirna_to_conll.py $DATA_DIR/miRNA_train.xml Diseases $DISEASE_DIR/miRNA2.conll &

# NCBI
python3 $SCRIPT_DIR/ncbi_diseases_to_conll.py $DATA_DIR/ncbi/NCBIdevelopset_corpus.txt $DISEASE_DIR/ncbi1.conll &
python3 $SCRIPT_DIR/ncbi_diseases_to_conll.py $DATA_DIR/ncbi/NCBItrainset_corpus.txt.patched $DISEASE_DIR/ncbi2.conll &
python3 $SCRIPT_DIR/ncbi_diseases_to_conll.py $DATA_DIR/ncbi/NCBItestset_corpus.txt $DISEASE_DIR/ncbi3.conll &

# Osiris
python3 $SCRIPT_DIR/osiris_gene_to_conll.py $DATA_DIR/osiris ge $GENE_DIR/osiris.conll &

# S800
python3 $SCRIPT_DIR/S800_species_to_conll.py "$DATA_DIR/s800" "$SPECIES_DIR/s800.conll" &

# SCAI Chemicals
python3 $SCRIPT_DIR/scai_to_conll.py "$DATA_DIR/scai_chemicals.conll" "$CHEMICAL_DIR/scai_chemicals.conll" &

# SCAI Diseases
python3 $SCRIPT_DIR/scai_to_conll.py "$DATA_DIR/scai_diseases.conll" "$DISEASE_DIR/scai_diseases.conll" &

# Variome
python3 $SCRIPT_DIR/variome_to_conll.py "$DATA_DIR/variome.xml.patched" "$GENE_DIR/variome.conll" gene &
python3 $SCRIPT_DIR/variome_to_conll.py "$DATA_DIR/variome.xml.patched" "$DISEASE_DIR/variome.conll" Disorder,disease &
python3 $SCRIPT_DIR/variome_to_conll.py "$DATA_DIR/variome.xml.patched" "$SPECIES_DIR/variome.conll" Living_Beings &

wait

cat $DISEASE_DIR/cdr1.conll $DISEASE_DIR/cdr2.conll $DISEASE_DIR/cdr3.conll > $DISEASE_DIR/cdr.conll
rm $DISEASE_DIR/cdr1.conll $DISEASE_DIR/cdr2.conll $DISEASE_DIR/cdr3.conll
cat $CHEMICAL_DIR/cdr1.conll $CHEMICAL_DIR/cdr2.conll $CHEMICAL_DIR/cdr3.conll > $CHEMICAL_DIR/cdr.conll
rm $CHEMICAL_DIR/cdr1.conll $CHEMICAL_DIR/cdr2.conll $CHEMICAL_DIR/cdr3.conll
cat $CHEMICAL_DIR/cemp1.conll $CHEMICAL_DIR/cemp2.conll > $CHEMICAL_DIR/cemp.conll
rm $CHEMICAL_DIR/cemp1.conll $CHEMICAL_DIR/cemp2.conll
cat $CHEMICAL_DIR/chemdner1.conll $CHEMICAL_DIR/chemdner2.conll $CHEMICAL_DIR/chemdner3.conll > $CHEMICAL_DIR/chemdner.conll
rm $CHEMICAL_DIR/chemdner1.conll $CHEMICAL_DIR/chemdner2.conll $CHEMICAL_DIR/chemdner3.conll
cat $GENE_DIR/gpro1.conll $GENE_DIR/gpro2.conll > $GENE_DIR/gpro.conll
rm $GENE_DIR/gpro1.conll $GENE_DIR/gpro2.conll
cat $DISEASE_DIR/ncbi1.conll $DISEASE_DIR/ncbi2.conll $DISEASE_DIR/ncbi3.conll > $DISEASE_DIR/ncbi.conll
rm $DISEASE_DIR/ncbi1.conll $DISEASE_DIR/ncbi2.conll $DISEASE_DIR/ncbi3.conll
cat $GENE_DIR/miRNA1.conll $GENE_DIR/miRNA2.conll > $GENE_DIR/miRNA.conll
rm $GENE_DIR/miRNA1.conll $GENE_DIR/miRNA2.conll
cat $SPECIES_DIR/miRNA1.conll $SPECIES_DIR/miRNA2.conll > $SPECIES_DIR/miRNA.conll
rm $SPECIES_DIR/miRNA1.conll $SPECIES_DIR/miRNA2.conll
cat $DISEASE_DIR/miRNA1.conll $DISEASE_DIR/miRNA2.conll > $DISEASE_DIR/miRNA.conll
rm $DISEASE_DIR/miRNA1.conll $DISEASE_DIR/miRNA2.conll
cat $GENE_DIR/bc2gm1.conll $GENE_DIR/bc2gm2.conll > $GENE_DIR/bc2gm.conll
rm $GENE_DIR/bc2gm1.conll $GENE_DIR/bc2gm2.conll
sed -i 's/Cell-line-name/NP/' $CELLLINE_DIR/gellus.conll

echo "Splitting corpora"
./split_corpora.sh

echo "Finished!"