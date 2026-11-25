import argparse
import json
from pathlib import Path

import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("results", type=Path)
parser.add_argument("html", type=Path)
args=parser.parse_args()
p=args.results


def records(name, columns=None):
    frame=pd.read_csv(p/(name+".csv"))
    return json.loads((frame[columns] if columns else frame).to_json(orient="records",double_precision=12))


profiles=pd.read_csv(p/"wave_profiles.csv")
stats=pd.read_csv(p/"wave.csv").query("L==256 and courant==.45 and seed==1")
wave=[]
for row in stats.itertuples():
    match=profiles[(profiles.stage==row.stage)&((profiles.t-row.t).abs()<1e-8)]
    wave.append({"stage":row.stage,"t":row.t,"entropy_delta":row.entropy_delta,
                 "energy":match.sort_values("i").energy.round(8).tolist()})

data={"ratchet":records("ratchet"),"forest":records("forest_kl"),"stationarity":records("stationarity"),
      "casimir":records("casimir",["dim","L","mass","r","strength","free","force","energy_cov"]),
      "casimir_mc":records("casimir_mc"),"replication":records("shared_validation_kl"),
      "words":pd.read_csv(p/"shared_words.csv",dtype={"word":str}).to_dict(orient="records"),"frames":json.loads((p/"metric_frames.json").read_text()),
      "wave":wave}
template=Path(__file__).with_name("lab.html.in").read_text()
args.html.write_text(template.replace("__EMBEDDED_DATA__",json.dumps(data,separators=(",",":"))))
