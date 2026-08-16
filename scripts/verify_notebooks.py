#!/usr/bin/env python3
"""verify_notebooks.py - checks every code cell of all Question notebooks for
error outputs and prints the first line of each code cell."""
import glob
import sys
from nbformat import read

root = r"D:\امتحان"
total = 0
for f in sorted(glob.glob(root + r"\Question_*\*.ipynb")):
    nb = read(f, as_version=4)
    q = f.split("Question_")[1].split("\\")[0]
    errs = 0
    print("=" * 60)
    print(q, "-", f.split("\\")[-1])
    for i, c in enumerate(nb.cells):
        if c.cell_type != "code":
            continue
        first = c.source.strip().split("\n")[0][:70]
        has_err = any(o.output_type == "error" for o in (c.outputs or []))
        mark = "ERR" if has_err else "OK "
        print(" [%s] %2d | %s" % (mark, i, first))
        errs += 1 if has_err else 0
    total += errs
print("=" * 60)
print("TOTAL ERROR CELLS:", total)
sys.exit(1 if total else 0)