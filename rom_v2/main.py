"""Thin executable entrypoint for ROM V2.

Supports both ``python -m rom_v2.main`` and direct IDE execution of this file.
Runtime composition belongs to ``rom_v2.app.runtime_launcher``.
"""
from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rom_v2.app.runtime_launcher import main

if __name__ == "__main__":
    raise SystemExit(main())
