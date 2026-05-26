# UILogParser
Parsing logs from the ubiquity logs

## Usage

Run the unified parser from `src/main.py`:

```powershell
python .\src\main.py
```

To enable AbuseIPDB enrichment, pass `--abuse-key YOUR_API_KEY`.

Options:
- `--db-patterns`: Glob patterns for .DB files (default: `\\DISKSTATION\DataStore\Logs\3RDAVE\*.DB`)
- `--output`: Output CSV for IP counts (default: `d:\RouterLogs\IPs.csv`)
- `--abuse-output`: Output CSV for enriched data (default: `d:\RouterLogs\IPs_abuse.csv`)
- `--max-db-files`: Limit number of DB files to process
- `--max-abuse-queries`: Limit AbuseIPDB API calls (default: 500)
