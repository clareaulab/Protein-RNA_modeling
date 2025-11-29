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


After generating relaxed structures and scoring the wild-type and all MGH mutants, the next step is to aggregate all results and perform statistical comparisons of interaction energies across variants.

Combine All Scores Across WT and Mutants

To merge the results from every run—including wild-type (WT) and all MGH mutants—use:

Replicate_Simulation/score_rnp.sh

This script collects and organizes Rosetta scoring outputs (interaction energies, ddG, etc.).

It internally calls:

Replicate_Simulation/get_lowest_scoring_ddgBind_relaxed_models.py

Important:

The Python script get_lowest_scoring_ddgBind_relaxed_models.py must be placed in:

$ROSETTA/source/src/apps/public/rnp_ddg/

to allow Rosetta to locate and execute it correctly.

Once all results are combined, we perform the main comparative analysis using:

compare_summaries_IE.sh
This wrapper script calls:

compare_summaries_IE.py

compare_summaries_IE.py:-extracts interaction energies (IntE)
-selects the top 40 models for each variant (sorted by Rosetta Score)
-computes mean ± SD per variant
-performs a Kruskal–Wallis test across all groups
-performs Dunn’s post-hoc pairwise comparisons (Bonferroni-adjusted)
-reports statistical differences between WT and each mutant



📘 _compare_summaries_IE.py_
compare_summaries_IE.py is a lightweight analysis tool for comparing Interaction Energy (IntE) across multiple Rosetta or design-pipeline output folders. It processes multiple subdirectories—each containing a summary.csv file—and extracts the top 40 models ranked by Score for each group. From these filtered models, the script:
1. Extracts Interaction Energies
Reads the top-N (default: 40 (ref: https://docs.rosettacommons.org/docs/latest/getting_started/Analyzing-Results,https://docs.rosettacommons.org/docs/latest/application_documentation/rna/rnp-ddg) models per group, sorted by the Score column. 
Pulls the IntE (Interaction Energy) column for those models.
Outputs raw IntE values (if --raw_intE is provided).
2. Computes Summary Statistics
Calculates the mean and standard deviation of IntE for each group.
Generates a publication-ready bar plot showing mean ± SD across groups.
3. Performs Non-Parametric Statistical Testing (Optional)
If --stats_vs_relax is specified:
Runs a global Kruskal–Wallis test across all groups to assess overall differences.
Performs Dunn’s post-hoc pairwise multiple comparisons (Bonferroni-corrected), reporting only comparisons vs a designated reference group (relax_2leb_WT).
Saves statistical results (group sizes, means, Kruskal–Wallis p-value, Dunn adjusted p-values) to a CSV file.



