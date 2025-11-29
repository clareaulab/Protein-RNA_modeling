#!/usr/bin/env python
from __future__ import print_function

import os
import csv
import argparse

import numpy as np
import matplotlib.pyplot as plt

# SciPy for Kruskal–Wallis
try:
    from scipy import stats
except ImportError:
    stats = None

TOP_N = 40
SCORE_COL = "Score"
INTE_COL = "IntE"
BASELINE_GROUP = "relax_2leb_WT"


# ----------------------------------------------------------
# Helpers to read summary.csv and select top-N by Score
# ----------------------------------------------------------

def read_summary_rows(summary_path):
    """Read summary.csv and find the first blank row (splits detail/stats blocks)."""
    with open(summary_path, "r") as f:
        rows = list(csv.reader(f))

    split_idx = None
    for i, row in enumerate(rows):
        if not any(cell.strip() for cell in row):
            split_idx = i
            break

    return rows, split_idx


def get_topN_by_score(rows, split_idx, score_col=SCORE_COL, top_n=TOP_N):
    """Return header and top-N rows sorted by Score ascending."""
    if split_idx is None or split_idx < 2:
        return None, []

    header = rows[0]
    detail_rows = rows[1:split_idx]

    try:
        score_idx = header.index(score_col)
    except ValueError:
        # No Score column; just return all rows as-is
        return header, detail_rows

    def get_score(r):
        try:
            return float(r[score_idx])
        except Exception:
            return float("inf")

    sorted_rows = sorted(detail_rows, key=get_score)
    sorted_rows = sorted_rows[:min(len(sorted_rows), top_n)]
    return header, sorted_rows


# ----------------------------------------------------------
# Extract IntE for top 40 per group
# ----------------------------------------------------------

def collect_intE_topN(root_dir):
    """
    For each group (subdirectory), extract top-N by Score
    and pull IntE values only.

    Returns:
        intE_data: dict[group -> [IntE values]]
    """
    intE_data = {}

    for name in sorted(os.listdir(root_dir)):
        d = os.path.join(root_dir, name)
        summary = os.path.join(d, "summary.csv")

        if not os.path.isdir(d) or not os.path.isfile(summary):
            continue

        rows, split_idx = read_summary_rows(summary)
        header, top_rows = get_topN_by_score(rows, split_idx)

        if not header or not top_rows:
            continue

        try:
            inte_idx = header.index(INTE_COL)
        except ValueError:
            print("No '{}' column found in {} — skipping".format(INTE_COL, summary))
            continue

        vals = []
        for r in top_rows:
            if len(r) <= inte_idx:
                continue
            cell = r[inte_idx]
            try:
                vals.append(float(cell))
            except Exception:
                continue

        if vals:
            intE_data[name] = vals
            print("Group {:20s} | Top-N IntE count = {}".format(name, len(vals)))

    return intE_data


# ----------------------------------------------------------
# Plotting: mean ± std of IntE across groups
# ----------------------------------------------------------

def plot_intE(intE_data, outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    groups = sorted(intE_data.keys())
    means = []
    stds = []

    for g in groups:
        arr = np.asarray(intE_data[g], dtype=float)
        means.append(float(np.mean(arr)))
        stds.append(float(np.std(arr, ddof=1) if arr.size > 1 else 0.0))

    fig, ax = plt.subplots()
    ax.bar(groups, means, yerr=stds, capsize=5)
    ax.set_ylabel(INTE_COL)
    ax.set_title("Interaction Energy ({}; top {} by {})".format(
        INTE_COL, TOP_N, SCORE_COL
    ))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    out_png = os.path.join(outdir, "comparison_IntE.png")
    plt.savefig(out_png)
    plt.close(fig)
    print("Wrote {}".format(out_png))


# ----------------------------------------------------------
# Raw IntE CSV
# ----------------------------------------------------------

def write_raw_intE(intE_data, out_csv):
    groups = sorted(intE_data.keys())
    max_len = max(len(v) for v in intE_data.values())

    with open(out_csv, "w") as f:
        w = csv.writer(f)
        w.writerow(groups)
        for i in range(max_len):
            row = []
            for g in groups:
                vals = intE_data[g]
                if i < len(vals):
                    row.append("{:.6f}".format(vals[i]))
                else:
                    row.append("")
            w.writerow(row)

    print("Wrote raw IntE to {}".format(out_csv))


# ----------------------------------------------------------
# Kruskal–Wallis + Dunn (Bonferroni) vs relax_2leb_WT
# ----------------------------------------------------------

def run_stats_vs_relax(intE_data, out_csv):
    """
    Do:
      1) Kruskal–Wallis test across all groups (global non-parametric test).
      2) Dunn's post-hoc pairwise comparisons (Bonferroni-adjusted),
         but only report comparisons vs BASELINE_GROUP.
    """
    if stats is None:
        print("SciPy not available — cannot run Kruskal–Wallis/Dunn tests.")
        return

    try:
        import scikit_posthocs as sp
    except ImportError:
        print("scikit-posthocs not available — install it to run Dunn's test.")
        return

    groups = sorted(intE_data.keys())
    if BASELINE_GROUP not in intE_data:
        print("Baseline group '{}' missing — stats skipped.".format(BASELINE_GROUP))
        return

    # Per-group arrays in fixed order
    arrays = [np.asarray(intE_data[g], dtype=float) for g in groups]

    # Global Kruskal–Wallis test
    H, p_global = stats.kruskal(*arrays)
    print("Kruskal–Wallis: H = {:.4f}, p = {:.4e}".format(H, p_global))

    # Dunn's post-hoc with Bonferroni correction
    # Here we use the "list of arrays" interface.
    pmat = sp.posthoc_dunn(arrays, p_adjust='bonferroni')
    # pmat index/columns are 1..K corresponding to order in `arrays` / `groups`

    baseline_arr = arrays[groups.index(BASELINE_GROUP)]
    mean_base = float(np.mean(baseline_arr))
    n_base = baseline_arr.size

    with open(out_csv, "w") as f:
        w = csv.writer(f)
        w.writerow([
            "stat",
            "baseline_group",
            "other_group",
            "n_baseline",
            "n_other",
            "mean_baseline",
            "mean_other",
            "kruskal_H_global",
            "kruskal_p_global",
            "dunn_p_adj"
        ])

        baseline_idx = groups.index(BASELINE_GROUP) + 1  # 1-based in pmat

        for g in groups:
            if g == BASELINE_GROUP:
                continue

            arr = np.asarray(intE_data[g], dtype=float)
            n_other = arr.size
            if n_other == 0:
                continue

            mean_other = float(np.mean(arr))

            other_idx = groups.index(g) + 1  # 1-based in pmat

            try:
                p_dunn = pmat.loc[baseline_idx, other_idx]
            except KeyError:
                p_dunn = float("nan")

            w.writerow([
                INTE_COL,
                BASELINE_GROUP,
                g,
                n_base,
                n_other,
                "{:.6f}".format(mean_base),
                "{:.6f}".format(mean_other),
                "{:.6f}".format(H),
                "{:.6e}".format(p_global),
                "{:.6e}".format(p_dunn),
            ])

    print("Wrote Kruskal–Wallis + Dunn stats vs {} to {}".format(
        BASELINE_GROUP, out_csv
    ))

# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Process Interaction Energy (IntE) of top {} models by Score, with optional Kruskal–Wallis + Dunn vs {}.".format(
            TOP_N, BASELINE_GROUP
        )
    )

    parser.add_argument(
        "-d", "--root_dir", default=".",
        help="Directory whose subdirs contain summary.csv files"
    )
    parser.add_argument(
        "-p", "--out_plots", default="./plots",
        help="Directory for output plots"
    )

    # Keep original interface:
    parser.add_argument("--raw_intE", help="Output CSV for raw IntE values")
    parser.add_argument("--raw_ddg", help="(Ignored) For interface compatibility")
    parser.add_argument("--raw_custom", help="(Ignored) For interface compatibility")

    parser.add_argument(
        "--stats_vs_relax",
        help="Output CSV for Kruskal–Wallis + Dunn stats vs {}".format(BASELINE_GROUP)
    )

    args = parser.parse_args()

    # Extract IntE values (top 40 by Score per group)
    intE_data = collect_intE_topN(args.root_dir)
    if not intE_data:
        print("No IntE data found.")
        return

    # Plot IntE means/std
    plot_intE(intE_data, args.out_plots)

    # Raw IntE CSV
    if args.raw_intE:
        write_raw_intE(intE_data, args.raw_intE)

    # Kruskal–Wallis + Dunn
    if args.stats_vs_relax:
        run_stats_vs_relax(intE_data, args.stats_vs_relax)


if __name__ == "__main__":
    main()
