"""Rebuild plants.jsonl from existing messages (no API calls). Use after changing build_plants.

    python -m sim.rebuild_plants                  # all workspaces
    python -m sim.rebuild_plants --ws ando
"""
import argparse
import json
from pathlib import Path

from sim.run_workspace import build_plants, load


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws", default="ando,anthropic,openai,xai")
    for ws in ap.parse_args().ws.split(","):
        base = Path(f"data/workspaces/{ws}")
        msgs = [json.loads(l) for l in (base / "messages.jsonl").read_text().splitlines()]
        plants = build_plants(load(ws), msgs)
        (base / "plants.jsonl").write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in plants))
        print(f"{ws}: {len(plants)} plants/decoys rebuilt")


if __name__ == "__main__":
    main()
