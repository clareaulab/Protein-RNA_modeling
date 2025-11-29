#!/bin/bash

# Activate the conda environment
source /data1/lareauc/users/dozica/Miniconda3/etc/profile.d/conda.sh
conda activate pdtk_general

# User-specified inputs (edit these as needed)
INPUT="2leb_uCCAGu_WT.pdb"
RESIDUE_NO=105
new="u"
OUTPUT="2leb-WT.pdb"
SCRIPT="Mutate_RNA.py"

# Run the Python script with the specified arguments
python "$SCRIPT" --input "$INPUT" --residue_no "$RESIDUE_NO" --output "$OUTPUT" --new "$new"
