In the wet-lab experiments, we used SRSF2 bound to uCCUGu RNA. The available crystal structure, however, is SRSF2 bound to uCCAGu (PDB ID: 2LEB). To match the experimental system, we first mutate the RNA and then introduce MGH mutants on SRSF2.

Mutate RNA in 2LEB (A → U)

Start from the original 2LEB structure (SRSF2 + uCCAGu).

To convert the RNA sequence from uCCAGu to uCCUGu, we mutate the 105th adenine to uracil.

This is done by running:
Replicate_Simulation/Mutate_RNA.sh

This script modifies residue 105 (A → U) and writes out:

2leb_WT.pdb

2leb_WT.pdb is the wild-type SRSF2–uCCUGu complex, matching the RNA used in experiments.

Generate MGH Mutants (R5, R61, R91, R94)

Starting from 2leb_WT.pdb, we introduce MGH substitutions at key arginine positions:

R5

R61

R91

R94

These mutations are created using the Jupyter notebook:
codes_to_mutate_2leb.ipynb

This notebook takes 2leb_WT.pdb as input and generates the corresponding MGH mutant structures for downstream Rosetta analysis.

Relax and Score Complexes with rnp_ddg

Once the wild-type and mutant structures are prepared, we perform energy minimization/relaxation and scoring using Rosetta’s rnp_ddg protocol.

This is done via:

Replicate_Simulation/relax_and_score_rnp_ddg.sh

This script internally calls:

relax_and_score_starting_structure.py
Note: relax_and_score_starting_structure.py is a custom application that should be added to:

$ROSETTA/source/src/apps/public/rnp_ddg/

Running relax_and_score_rnp_ddg.sh generates a helper script:

run_ALL_RELAX_COMMANDS.sh

You can then launch all relax/score jobs by executing:

bash run_ALL_RELAX_COMMANDS.sh

This will carry out the relaxation and scoring for the wild-type and all MGH mutants, producing the Rosetta score files used for downstream analysis.

