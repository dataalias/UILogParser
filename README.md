# UILogParser
Parsing logs from the ubiquity logs

## Pipeline

Run the scripts in `src/` in this order:

1. **`ips_to_file.py`** reads the Ubiquiti syslog SQLite DB, extracts every public IPv4 address, and writes `d:\RouterLogs\IPs.csv` (`ip,count`). Edit `connection_string` to point at the log DB first.
2. **`iprep.py`** looks up each IP with `count >= 20` on AbuseIPDB (max 500 lookups) and writes `d:\RouterLogs\IPs_output.csv`, which includes `abuseConfidenceScore`.
3. **`abuse_filter.py`** filters the abuse CSV and pushes the bad IPs to the UDM Pro deny list (see below).

## Filtering abusive IPs into a mongo script for the UDM Pro deny list

`src/abuse_filter.py` selects IPs with `abuseConfidenceScore >= 50` and `count > 100` and builds a mongo script that adds them to the `DenyListIPAddresses` firewall group.

| Function | Purpose |
|----------|---------|
| `get_abusive_ips(file_name, min_score=50, min_count=100)` | Returns the list of matching IPs from the abuse CSV. |
| `abusive_ips_to_mongo_script(file_name, script_file_name=None, list_name="DenyListIPAddresses", min_score=50, min_count=100)` | Writes the mongo script `<input>_denylist.js` with the IPs embedded, and returns the IPs. |

### Usage

1. Generate the script:
   ```
   python src/abuse_filter.py
   ```
   This reads `d:\RouterLogs\IPs_output.csv` and writes `d:\RouterLogs\IPs_output_denylist.js`.
2. Copy it to the UDM and run it:
   ```
   scp d:\RouterLogs\IPs_output_denylist.js root@<udm-ip>:/root/
   ssh root@<udm-ip> "mongo --port 27117 ace < /root/IPs_output_denylist.js"
   ```
3. Restart the UniFi controller so it reloads the DB: `systemctl restart unifi` on the UDM.

### What the generated script does

1. Aborts unless exactly one `firewallgroup` is named `DenyListIPAddresses`.
2. Prints the current group document (backup).
3. Runs `$addToSet` with `$each` on `group_members` (no duplicates).
4. Prints the update result and the updated document.

Every IP is validated as IPv4 before it is written to the script.

### Prerequisites and warnings

- SSH must be enabled on the UDM (Settings -> System -> Advanced).
- The `DenyListIPAddresses` group must already exist; the script will not create it.
- Direct DB edits can be overwritten by the controller. For a full backup first, run `mongodump --port 27117 --db ace --out /root/backup-$(date +%Y%m%d)` on the UDM.
- More detail on the MongoDB commands is in [docs/Mongo.md](docs/Mongo.md).
