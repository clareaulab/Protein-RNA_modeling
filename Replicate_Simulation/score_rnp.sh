#!/usr/bin/env bash
set -euo pipefail

# adjust these if you like, or pass them in as args
BASE_DIR="/data1/lareauc/users/dozica/Collaborations/SRSF2-RNA/Scripts/rnp_ddg/All_Data"
SCRIPT="/data1/lareauc/users/dozica/Software/rosetta/source/src/apps/public/rnp_ddg/get_lowest_scoring_ddgBind_relaxed_models.py"
N=40

for RELAX_DIR in "$BASE_DIR"/*/; do
  # skip anything that isn’t a directory
  [ -d "$RELAX_DIR" ] || continue

  echo "=== Processing $(basename "$RELAX_DIR") ==="
  python "$SCRIPT" --relax_dir "$RELAX_DIR" -n "$N"
done
