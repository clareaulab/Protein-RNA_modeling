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
build models of ncAAs,
prepare .sdf/.sif inputs for Rosetta,
generate .params files and rotamer libraries,
and integrate the new residues into Rosetta.
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


⚠️ Note:
The workflows in this repository require a working installation of the Rosetta macromolecular modeling suite.
Rosetta is available for academic use at:
https://www.rosettacommons.org/software

