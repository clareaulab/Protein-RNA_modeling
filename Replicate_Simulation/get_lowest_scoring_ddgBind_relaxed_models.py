#!/usr/bin/env python2
from __future__ import print_function

import argparse
import os
import glob
import math
import csv


def stats(vals):
    m = sum(vals) / len(vals)
    v = sum((x - m) ** 2 for x in vals) / len(vals)
    return m, math.sqrt(v)


def main(args):
    if not os.path.exists(args.relax_dir):
        print("ERROR: %s does not exist!" % args.relax_dir)
        return

    # decide output CSV path
    out_csv = args.out or os.path.join(args.relax_dir, 'summary.csv')

    records = []
    for rdir in os.listdir(args.relax_dir):
        full_d = os.path.join(args.relax_dir, rdir)
        if not os.path.isdir(full_d) or rdir == 'input_lists':
            continue

        pdbs = glob.glob(os.path.join(full_d, 'min_again*pdb'))
        if not pdbs:
            continue
        pdb = pdbs[0]

        logpath = os.path.join(full_d, 'relax_2.log')
        if not os.path.exists(logpath):
            continue

        score = ddg_bind = inter_E = unbound_RNA = unbound_prot = None
        for line in open(logpath):
            if "Score of the complex" in line:
                try:
                    score = float(line.split()[-1])
                except ValueError:
                    pass
            elif "ddG_bind" in line:
                try:
                    ddg_bind = float(line.split()[-1])
                except ValueError:
                    pass
            elif "Interaction energy of complex" in line:
                try:
                    inter_E = float(line.split()[-1])
                except ValueError:
                    pass
            elif "Unbound RNA score" in line:
                try:
                    unbound_RNA = float(line.split()[-1])
                except ValueError:
                    pass
            elif "Unbound protein score" in line:
                try:
                    unbound_prot = float(line.split()[-1])
                except ValueError:
                    pass
            if None not in (score, ddg_bind, inter_E, unbound_RNA, unbound_prot):
                break

        if score is not None:
            records.append((score, ddg_bind, inter_E, unbound_RNA, unbound_prot, pdb))

    n = min(len(records), args.nmodels)
    topN = sorted(records, key=lambda x: x[0])[:n]

    # Collect values for statistics
    ddg_vals, ie_vals, prot_vals, urna_vals, custom_vals = [], [], [], [], []

    # Write both detail table and stats into CSV
    with open(out_csv, 'w') as csvf:
        w = csv.writer(csvf)
        # header for top models
        w.writerow(["Rank", "Score", "ddG_bind", "IntE", "Unbound_RNA", "Unbound_Prot", "ΔG_custom", "PDB"])
        for rank, (scr, ddg, ie, urna, uprot, pdbf) in enumerate(topN):
            custom = None
            if None not in (ie, uprot, urna):
                # you said you wanted Score in the custom formula here
                custom = 0.38 * scr - 0.38 * uprot - 0.28 * urna

            w.writerow([
                rank,
                "%.3f" % scr,
                "%.3f" % ddg,
                "%.3f" % ie,
                "%.3f" % urna,
                "%.3f" % uprot,
                ("%.3f" % custom) if custom is not None else "",
                pdbf
            ])

            ddg_vals.append(ddg)
            ie_vals.append(ie)
            prot_vals.append(uprot)
            urna_vals.append(urna)
            if custom is not None:
                custom_vals.append(custom)

        # blank line then summary stats
        w.writerow([])
        w.writerow(["Statistic", "Mean", "StdDev"])
        if ddg_vals:
            m_ddg, s_ddg = stats(ddg_vals)
            w.writerow(["ddG_bind", "%.3f" % m_ddg, "%.3f" % s_ddg])
        if ie_vals:
            m_ie, s_ie = stats(ie_vals)
            w.writerow(["Interaction energy", "%.3f" % m_ie, "%.3f" % s_ie])
        if prot_vals:
            m_prot, s_prot = stats(prot_vals)
            w.writerow(["Unbound protein", "%.3f" % m_prot, "%.3f" % s_prot])
        if urna_vals:
            m_urna, s_urna = stats(urna_vals)
            w.writerow(["Unbound RNA", "%.3f" % m_urna, "%.3f" % s_urna])
        if custom_vals:
            m_cust, s_cust = stats(custom_vals)
            w.writerow(["ΔG_custom", "%.3f" % m_cust, "%.3f" % s_cust])

    print("Wrote detailed results + summary to %s" % out_csv)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract scores + compute custom ΔG")
    parser.add_argument('-r', '--relax_dir', required=True,
                        help='Directory containing relax run results')
    parser.add_argument('-n', '--nmodels', type=int, default=20,
                        help='Number of top‐scoring models to report')
    parser.add_argument('-o', '--out',
                        help='Path to CSV file to write results (default: <relax_dir>/summary.csv)')
    args = parser.parse_args()
    main(args)
