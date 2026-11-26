"""Embed verified results in a standalone offline laboratory."""
import csv
import json
from pathlib import Path


root = Path(__file__).resolve().parent
names = ("product", "radion", "sheared_waves", "slab")
data = {}
for name in names:
    with (root / "results" / (name+".csv")).open() as file:
        rows = list(csv.DictReader(file))
        if name == "radion":
            rows = [row for row in rows if int(row["n"]) == 2 and
                    round(float(row["time"])*40)%4 == 0]
        data[name] = rows
template = (root/"lab.html.in").read_text()
(root/"lab.html").write_text(template.replace("__RESULTS__", json.dumps(data, separators=(",", ":"))))
