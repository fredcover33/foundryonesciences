# stock-picker

Deterministic day-trading scanner ("the picker").

## Block 0 — scaffold + Massive Flat Files feasibility probe

Block 0 builds nothing that trades. It measures, empirically:

- which Massive plan tier carries the stocks flat-file datasets,
- how far back each tier reaches,
- how large the daily files are,
- how long they take to download and parse.

No purchase, no orders, no brokerage connection, no live or delayed API feed.

## Layout

    src/picker/config.py      strict config loader (no defaults in code)
    src/picker/flatfiles.py   Massive Flat Files access
    src/picker/storage.py     SQLite store for parsed aggregates
    docs/DATA_SOURCES.md      documentation survey, with quotes
    docs/DECISIONS.md         decisions log
    docs/FEASIBILITY.md       measured extrapolation
    config.toml               all tunables; a missing key is fatal

## Setup

    python -m venv .venv
    .venv/bin/pip install -r requirements.txt

Copy `.env.example` to `.env` and fill in the S3 credentials. `.env` is
gitignored and must never be committed.
