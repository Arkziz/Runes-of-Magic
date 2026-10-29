"""Allow ``python -m rom_v2`` as the shortest canonical launch command."""
from rom_v2.app.runtime_launcher import main

if __name__ == "__main__":
    raise SystemExit(main())
