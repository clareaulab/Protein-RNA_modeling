# Protein-RNA modeling

This repository contains code and workflows for performing RNA–protein modeling in Rosetta, including:
mutation of residues in RNA and protein,
introduction and parameterization of non-canonical amino acids (ncAAs), and
scoring protein–RNA complexes using Rosetta’s rnp-ddg energy function (weights specialized for RNA–protein interaction).
These tools and workflows were developed as part of the manuscript:
Non-Enzymatic MGO-Glycation of SRSF2 Drives RNA Mis-Splicing in Cancer
Xiao et al. (2025)
The repository is organized into two major components:

1. Non-Canonical Amino Acid (ncAA) Generation

Directory: Protein-RNA_modeling/Create_Rotamer_Library/
This section shows how to:
build chemically accurate models of ncAAs,
prepare .sdf/.sif inputs for Rosetta,
generate .params files and rotamer libraries,
and integrate the new residues into Rosetta’s polymer machinery.
These steps enable incorporation of MGO-modified amino acids (e.g., MGH) or any other custom residue into Rosetta simulations.

 2. RNA–Protein Binding Simulations Using rnp-ddg

Directory: Protein-RNA_modeling/Replicate_Simulation/
This portion of the workflow includes:
mutating bases in RNA or residues in the protein using Rosetta tools,
preparing mutant complexes (e.g., SRSF2 mutants bound to RNA),
relaxing and scoring structures with rnp-ddg.wts,
aggregating results across all variants,
and performing statistical analysis of interaction energies.
Together, these simulations support the computational analysis performed in the associated manuscript, enabling reproduction of all modeling steps involved in studying glycation-induced changes in SRSF2–RNA binding.





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
