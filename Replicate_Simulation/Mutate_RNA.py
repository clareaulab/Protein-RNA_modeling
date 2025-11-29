#!/usr/bin/env python

import argparse
import pyrosetta
from pyrosetta import pose_from_pdb, Pose
from pyrosetta.rosetta.core.pose.rna import mutate_position

def mutate_rna_pose(input_path, residue_no, new_base):
    """
    Load a structure from input_path, mutate the RNA residue at residue_no 
    to new_base (one-letter code), and return the mutated pose.
    """
    # Load the structure
    pose = pose_from_pdb(input_path)
    
    # Create a copy of the pose
    mutated_pose = Pose()
    mutated_pose.assign(pose)
    
    # Perform the mutation (new_base should be provided as lowercase or uppercase)
    mutate_position(mutated_pose, residue_no, new_base)
    
    return mutated_pose

def main():
    parser = argparse.ArgumentParser(
        description="Mutate an RNA residue in a given structure using PyRosetta."
    )
    parser.add_argument("--input", required=True, help="Path to input PDB structure.")
    parser.add_argument("--residue_no", type=int, required=True, help="Residue number to mutate.")
    parser.add_argument("--new", required=True, help="Target nucleotide (one-letter code, e.g., 'u').")
    parser.add_argument("--output", default="mutated_structure.pdb", help="Path to output PDB file.")
    args = parser.parse_args()

    # Initialize PyRosetta (you can add additional flags if necessary)
    pyrosetta.init("-ignore_zero_occupancy true")

    mutated_pose = mutate_rna_pose(args.input, args.residue_no, args.new)
    mutated_pose.dump_pdb(args.output)
    print(f"Mutated structure saved to {args.output}")

if __name__ == "__main__":
    main()
