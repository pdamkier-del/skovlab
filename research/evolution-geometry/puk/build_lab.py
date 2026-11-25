import argparse
import json
from pathlib import Path

import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument("results",type=Path)
parser.add_argument("html",type=Path)
args=parser.parse_args()


def csv(name):
    return pd.read_csv(args.results/f"{name}.csv")


def records(frame):
    return json.loads(frame.to_json(orient="records",double_precision=12))


data={
    "minimal":records(csv("minimal_summary")),
    "motifs":records(csv("motif_summary")),
    "interfaces":records(csv("interface_summary")),
    "equilibria":records(csv("motif_equilibria").query("donor==0")),
    "markov":records(csv("markov")),
}
template=Path(__file__).with_name("lab.html.in").read_text()
args.html.write_text(template.replace("__DATA__",json.dumps(data,separators=(",",":"))))
