"""Compare your pilot labels with the planted labels.   python -m label.check_pilot"""
import csv
import json

from label.context import load_ws


def main():
    key = {k["row"]: k for k in json.load(open("data/gold/pilot_20_key.json"))}
    mine = {int(r["row"]): r for r in csv.DictReader(open("label/pilot_20_labels.csv")) if r["label"].strip()}
    details = {}
    for ws in {k["point_id"].split("/")[0] for k in key.values()}:
        d = load_ws(ws)[0]
        for t in d["threads"]:
            for e in t["events"]:
                if e.get("id"):
                    details[e["id"]] = e.get("detail", "")
    graded = agree = 0
    print(f"{'row':>3}  {'kind':<14} {'yours':<10} {'planted':<10} note")
    for row in sorted(key):
        k, m = key[row], mine.get(row)
        yours = m["label"].strip().upper() if m else "-"
        gold = k["gold_label"] or "(none)"
        flag = ""
        if k["gold_label"] and m:
            graded += 1
            agree += yours == gold
            flag = "" if yours == gold else "  <-- differs"
        print(f"{row:>3}  {k['kind']:<14} {yours:<10} {gold:<10}{flag}")
        if flag:
            print(f"     {k['type']}: {details.get(k['plant_id'], '')}")
            if m and m["notes"].strip():
                print(f"     your note: {m['notes'].strip()}")
    print(f"\nagreement with planted labels: {agree}/{graded}"
          f"  (rows without a planted label are labeled by you; those become gold)")


if __name__ == "__main__":
    main()
