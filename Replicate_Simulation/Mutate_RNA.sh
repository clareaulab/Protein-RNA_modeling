#!/bin/bash

# Activate the conda environment
source /data1/lareauc/users/dozica/Miniconda3/etc/profile.d/conda.sh
conda activate pdtk_general

# User-specified inputs (edit these as needed)
INPUT="/data1/lareauc/users/dozica/Collaborations/SRSF2-RNA/Scripts/rnp_ddg/All_Data/2leb_uCCAGu_WT.pdb"
RESIDUE_NO=105
new="u"
OUTPUT="/data1/lareauc/users/dozica/Collaborations/2leb-WT-U-added.pdb"
SCRIPT="/data1/lareauc/users/dozica/Collaborations/SRSF2-RNA/Scripts/Mutate_RNA.py"

# Run the Python script with the specified arguments
python "$SCRIPT" --input "$INPUT" --residue_no "$RESIDUE_NO" --output "$OUTPUT" --new "$new"
