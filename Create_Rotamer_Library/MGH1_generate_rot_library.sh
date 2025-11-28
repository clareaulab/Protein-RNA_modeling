cd /Protein-RNA_modeling/Output_Files
python $ROSETTA/source/scripts/python/public/molfile_to_params_polymer.py  \
--clobber --polymer --no-pdb --name MGH --use-parent-rotamers ARG \
-i /Protein-RNA_modeling/Input_Files/MGH.sdf
