# CLAUDE.md

Python scripts that parse Ubiquiti router logs, score IPs with AbuseIPDB, and push abusive IPs to a UDM Pro deny list. See [README.md](README.md) for usage.

## Layout

- `src/ips_to_file.py` extracts IPs from the syslog SQLite DB to `IPs.csv` (`ip,count`).
- `src/iprep.py` enriches `IPs.csv` with AbuseIPDB scores to `IPs_output.csv`.
- `src/abuse_filter.py` filters by score and count, and updates the UDM Pro deny list.
- `src/main.py`, `src/x_main copy.py` are older experiments.
- `docs/Mongo.md` has the UDM Pro MongoDB commands (port 27117, db `ace`, collection `firewallgroup`).

## Conventions and gotchas

- `iprep.py` and `ips_to_file.py` call their main function at import time. Never import from them; put reusable code in a new module like `abuse_filter.py`.
- Paths are hardcoded Windows paths (`d:\RouterLogs\...`, `\\DISKSTATION\...`).
- Abuse CSV columns used: `ip`, `count`, `abuseConfidenceScore`.
- Filter thresholds: score `>= 50`, count `> 100`.
- The deny list is the `DenyListIPAddresses` group. Changes need `systemctl restart unifi` to take effect.
- `abusive_ips_to_mongo_script` only generates a `.js` file; it never touches the router. Running that script on the UDM modifies the live router, so do not do so without the user's explicit go-ahead.
- `iprep.py` has an AbuseIPDB API key hardcoded. Never print or copy it, and do not add more secrets to the repo.
- Update [CHANGELOG.md](CHANGELOG.md) with every user-visible change.
