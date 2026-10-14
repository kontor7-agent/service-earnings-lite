#!/usr/bin/env python3
"""service-earnings-lite: what does each service really leave you per hour?

Reads three CSV files (supplies, services, recipes), prints a table.
Standard library only. No network. Never modifies or deletes input files.
Writes a file only if you pass --out (and refuses to overwrite without --force).
"""
import argparse
import csv
import sys
from pathlib import Path


def read_csv(path, required):
    p = Path(path)
    if not p.is_file():
        sys.exit(f"File not found: {p}")
    with p.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
        cols = set(rows[0].keys()) if rows else set()
    missing = [c for c in required if c not in cols and rows]
    if missing:
        sys.exit(f"{p.name}: missing column(s): {', '.join(missing)}")
    return rows


def num(v, what, where):
    try:
        return float(str(v).strip().replace(",", "."))
    except ValueError:
        sys.exit(f"Not a number for {what} ({where}): {v!r}")


def compute(args):
    folder = Path(args.folder)
    supplies = {}
    for r in read_csv(folder / "supplies.csv", ["supply", "pack_size", "pack_price"]):
        size = num(r["pack_size"], "pack_size", r["supply"])
        if size <= 0:
            sys.exit(f"pack_size must be > 0 for {r['supply']}")
        supplies[r["supply"].strip().lower()] = num(r["pack_price"], "pack_price", r["supply"]) / size

    materials = {}
    for r in read_csv(folder / "recipes.csv", ["service", "supply", "quantity"]):
        key = r["supply"].strip().lower()
        if key not in supplies:
            sys.exit(f"recipes.csv: unknown supply {r['supply']!r} (service {r['service']!r})")
        s = r["service"].strip()
        materials[s] = materials.get(s, 0.0) + supplies[key] * num(r["quantity"], "quantity", s)

    fee = args.card_fee / 100.0
    out = []
    for r in read_csv(folder / "services.csv", ["service", "minutes", "price"]):
        name = r["service"].strip()
        minutes = num(r["minutes"], "minutes", name)
        price = num(r["price"], "price", name)
        if minutes <= 0:
            sys.exit(f"minutes must be > 0 for {name}")
        hours = minutes / 60.0
        mat = materials.get(name, 0.0)
        card = price * fee
        over = hours * args.overhead_per_hour
        left = price - mat - card - over
        per_hour = left / hours
        suggested = (mat + over + args.goal_per_hour * hours) / (1 - fee)
        if left < 0:
            status = "Loses money"
        elif per_hour < args.goal_per_hour:
            status = "Below goal"
        else:
            status = "Healthy"
        out.append({"service": name, "minutes": minutes, "price": price,
                    "materials": mat, "card_fee": card, "overhead": over,
                    "left": left, "left_per_hour": per_hour,
                    "suggested_price": suggested, "status": status})
    return out


def main():
    ap = argparse.ArgumentParser(description="Per-service earnings from simple CSV files.")
    ap.add_argument("folder", help="folder containing supplies.csv, services.csv, recipes.csv")
    ap.add_argument("--goal-per-hour", type=float, default=25.0, help="take-home goal per hour (default 25)")
    ap.add_argument("--overhead-per-hour", type=float, default=6.0,
                    help="rent + fixed costs per booked hour (default 6)")
    ap.add_argument("--card-fee", type=float, default=1.5, help="card fee in percent (default 1.5)")
    ap.add_argument("--out", help="optional: also write the result to this new CSV file")
    ap.add_argument("--force", action="store_true", help="allow overwriting --out")
    args = ap.parse_args()
    if not 0 <= args.card_fee < 100:
        sys.exit("--card-fee must be between 0 and 99.9")

    rows = compute(args)
    rows.sort(key=lambda r: r["left_per_hour"])
    print(f"{'Service':<28}{'Price':>8}{'Material':>9}{'Left':>8}{'Left/h':>8}{'Suggest':>9}  Status")
    for r in rows:
        print(f"{r['service'][:27]:<28}{r['price']:>8.2f}{r['materials']:>9.2f}"
              f"{r['left']:>8.2f}{r['left_per_hour']:>8.2f}{r['suggested_price']:>9.2f}  {r['status']}")
    print("\nSorted worst to best by 'Left/h'. Suggested price is a starting point, your decision.")

    if args.out:
        o = Path(args.out)
        if o.exists() and not args.force:
            sys.exit(f"{o} exists; use --force to overwrite.")
        with o.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            for r in rows:
                w.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
        print(f"Wrote {o}")


if __name__ == "__main__":
    main()
