# Protein-RNA modeling

README


Boltz-1
ncAA - code
ccd.pkl files
Biophysical parameters code, bindcraft environment ? 
input yml files, 
slurm script 





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
