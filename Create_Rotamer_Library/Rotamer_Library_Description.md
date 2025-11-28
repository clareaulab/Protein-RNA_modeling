
🧬 Creating a Non-Canonical Amino Acid (ncAA) and Rotamer Library in Rosetta
This section outlines the first step in generating a non-canonical amino acid (ncAA) for use in Rosetta: preparing the chemical structure and producing a .sdf / .sif file that Rosetta can convert into parameters and a rotamer library.
Rosetta supports multiple approaches for incorporating ncAAs (e.g., treating them as small molecules, deriving rotamers from existing libraries, or generating rotamers via CHARMM).
Here we follow the workflow recommended in Rosetta Commons demos.
1. Draw the ncAA and Generate an .sdf File
Start by creating a 3D structure of your new amino acid:
Open a molecular sketching tool such as the RCSB ChemSketch Tool:
https://www.rcsb.org/chemical-sketch
Draw your amino acid with terminal caps, as required by Rosetta:
N-terminal: N-acetyl cap (ACE)
C-terminal: N-methylamide (NME)
Ensure the residue is drawn as the backbone fragment of a peptide, with ACE–Residue–NME connectivity. This is required for Rosetta’s polymer machinery.
(See Rosetta’s ncAA design tutorial: https://docs.rosettacommons.org/demos/latest/public/design_with_ncaa/README)
Export the structure as an .sdf file.
2. Convert to .sif Format
Rosetta’s residue parameter generator uses .sif files (SMILES Input Format).
You can convert .sdf → .sif using:
Online OpenBabel converter:
https://www.cheminfo.org/Chemistry/Cheminformatics/FormatConverter/index.html
Download the resulting .sif file.
3. Add Rosetta Instructions to the .sif File
At the end of your .sif file, append a <RosettaParamsInstructions> block.
For the example residue MGH, the block looks like:


<RosettaParamsInstructions>
M  ROOT 17
M  POLY_N_BB 17
M  POLY_CA_BB 5
M  POLY_C_BB 3
M  POLY_O_BB 4
M  POLY_IGNORE 21 22 23 24 1 20 19 39 40 41
M  POLY_UPPER 2
M  POLY_LOWER 18
M  POLY_CHG 0
M  POLY_PROPERTIES PROTEIN POLYMER ALPHA_AA AROMATIC L_AA CYCLIC
M  END
