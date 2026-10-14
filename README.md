# service-earnings-lite

**Find out which of your services actually pay you – from three simple CSV files.**

For solo stylists, nail techs, lash artists and barbers. Enter what your supplies cost, which supplies each service uses and what you charge. The script shows material cost, card fee, your share of fixed costs, what is left per hour, and a suggested price, sorted worst to best.

## What it does
- Calculates cost per gram/ml/piece from pack size and pack price
- Adds up material cost per service from your recipes
- Subtracts card fee and fixed costs per booked hour
- Flags each service: `Healthy`, `Below goal` or `Loses money`
- Suggests a price that reaches your per-hour goal (a starting point – your decision)

## Quick start
```
python service_earnings.py sample --goal-per-hour 25 --overhead-per-hour 6 --card-fee 1.5
```
Then copy the `sample` folder, replace the CSV contents with your own, and run again. Optional: `--out result.csv` saves the table (refuses to overwrite without `--force`).

CSV columns:
- `supplies.csv`: `supply,unit,pack_size,pack_price`
- `services.csv`: `service,minutes,price`
- `recipes.csv`: `service,supply,quantity` (quantity in the supply's unit)

## Requirements
- Python 3.8+ (standard library only)
- No network access, no installs. Input files are only read, never changed or deleted.

## Notes
This is a calculator for your own numbers. It does not replace an accountant; rules on taxes and chair rent differ by country.

Created with AI assistance by an automated system.

## Full version
The lite version is a command-line calculator. The full kit is an Excel workbook (9 sheets, formulas, drop-downs, sample data) that additionally has:
- Settings for rent, other fixed costs, bookable hours and booked share – overhead is derived, not typed in
- Supplier price-change tracking (pack price before/now) with the effect on each service
- A self-filling, printable client Price List
- Daily Takings check of diary vs. cash, card and other money, with tips tracked separately and a monthly summary
- A No-Shows sheet: lost income, empty chair hours, repeat clients
- Quick-start PDF

Get it here: https://kontor7-agent.github.io/p/know-what-each-service-really-earns-product-cost?s=github
