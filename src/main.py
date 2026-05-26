import argparse
import csv
import glob
import re
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Iterable, List

DB_SEARCH_PATTERNS = [
    r"\\DISKSTATION\DataStore\Logs\3RDAVE\*.DB"
]
DEFAULT_OUTPUT_CSV = Path(r"d:\RouterLogs\IPs.csv")
DEFAULT_ABUSE_OUTPUT_CSV = Path(r"d:\RouterLogs\IPs_abuse.csv")
DEFAULT_QUERY = "SELECT * FROM logs"
IGNORE_IPS = {
    "127.0.0.1",
    "99.145.235.143",
    "8.8.8.8",
    "8.8.4.4",
    "1.1.1.1",
    "255.255.255.255",
    "233.89.188.1",
    "224.0.0.5",
    "224.0.0.251",
    "224.0.0.1",
    "0.0.0.0"
}
PRIVATE_PREFIXES = (
    "10.",
    "127.",
    "169.254.",
    "172.16.",
    "172.17.",
    "172.18.",
    "172.19.",
    "172.20.",
    "172.21.",
    "172.22.",
    "172.23.",
    "172.24.",
    "172.25.",
    "172.26.",
    "172.27.",
    "172.28.",
    "172.29.",
    "172.30.",
    "172.31.",
    "192.168.",
)
IPV4_REGEX = re.compile(
    r"\b(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b"
)


def find_db_files(patterns: List[str]) -> List[Path]:
    db_paths: List[Path] = []
    for pattern in patterns:
        matched = sorted(glob.glob(pattern))
        db_paths.extend(Path(path) for path in matched)
    return db_paths


def is_ignored_ip(ip_address: str) -> bool:
    if ip_address in IGNORE_IPS:
        return True
    return ip_address.startswith(PRIVATE_PREFIXES)


def extract_ips_from_record(record: Iterable, regex: re.Pattern) -> List[str]:
    ips: List[str] = []
    for value in record:
        if isinstance(value, str):
            ips.extend(regex.findall(value))
    return ips


def extract_ips_from_db(db_path: Path, query: str = DEFAULT_QUERY) -> Counter:
    ip_counter = Counter()
    connection = None
    try:
        connection = sqlite3.connect(str(db_path))
        connection.text_factory = lambda b: b.decode(errors="ignore")
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            for ip in extract_ips_from_record(row, IPV4_REGEX):
                if not is_ignored_ip(ip):
                    ip_counter[ip] += 1

    except sqlite3.Error as exc:
        print(f"Warning: failed to read {db_path}: {exc}")
    finally:
        if connection is not None:
            connection.close()

    return ip_counter


def write_ip_counts(ip_counts: Counter, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["ip", "count"])
        for ip, count in ip_counts.most_common():
            writer.writerow([ip, count])


def abuse_ipdb_enrich(
    input_file: Path,
    output_file: Path,
    api_key: str,
    min_count: int = 20,
    max_queries: int = 500,
) -> None:
    try:
        import requests
    except ImportError as exc:
        raise RuntimeError("requests is required for AbuseIPDB enrichment") from exc

    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Accept": "application/json",
        "Key": api_key,
    }
    params = {"ipAddress": None, "maxAgeInDays": "90"}

    with input_file.open("r", newline="", encoding="utf-8") as source, output_file.open(
        "w", newline="", encoding="utf-8"
    ) as dest:
        reader = csv.DictReader(source)
        fieldnames = [
            "ip",
            "count",
            "abuseConfidenceScore",
            "countryCode",
            "domain",
            "hostnames",
            "ipAddress",
            "ipVersion",
            "isPublic",
            "isTor",
            "isWhitelisted",
            "isp",
            "lastReportedAt",
            "numDistinctUsers",
            "totalReports",
            "usageType",
        ]
        writer = csv.DictWriter(dest, fieldnames=fieldnames)
        writer.writeheader()

        processed = 0
        for row in reader:
            if processed >= max_queries:
                break
            if int(row.get("count", "0")) < min_count:
                continue

            params["ipAddress"] = row["ip"]
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json().get("data", {})
            data["ip"] = row["ip"]
            data["ipAddress"] = row["ip"]
            data["count"] = row["count"]

            hostnames = data.get("hostnames", "")
            if isinstance(hostnames, list):
                data["hostnames"] = ";".join(str(item) for item in hostnames)

            writer.writerow({key: data.get(key, "") for key in fieldnames})
            processed += 1

    print(f"AbuseIPDB enrichment complete: {processed} addresses written to {output_file}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract IPs from Ubiquiti SQLite logs and optionally enrich counts with AbuseIPDB."
    )
    parser.add_argument(
        "--db-patterns",
        nargs="*",
        default=DB_SEARCH_PATTERNS,
        help="Glob patterns for .DB files to process.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_CSV,
        help="CSV file path for aggregated IP counts.",
    )
    parser.add_argument(
        "--abuse-output",
        type=Path,
        default=DEFAULT_ABUSE_OUTPUT_CSV,
        help="CSV file path for AbuseIPDB enrichment results.",
    )
    parser.add_argument(
        "--abuse-key",
        type=str,
        default="15d2eb74e34443f1781f9466437f336d7a70b6cb354e41cf9b85cbbe4521049b05891b9165641d6f",
        help="AbuseIPDB API key for optional enrichment.",
    )
    parser.add_argument(
        "--min-abuse-count",
        type=int,
        default=20,
        help="Minimum IP count to query AbuseIPDB.",
    )
    parser.add_argument(
        "--max-abuse-queries",
        type=int,
        default=500,
        help="Maximum AbuseIPDB queries to perform.",
    )
    parser.add_argument(
        "--query",
        type=str,
        default=DEFAULT_QUERY,
        help="SQL query to select log rows from the database.",
    )
    parser.add_argument(
        "--max-db-files",
        type=int,
        default=None,
        help="Maximum number of DB files to process (default: all).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    db_paths = find_db_files(args.db_patterns)

    if not db_paths:
        print("No database files found. Check DB_SEARCH_PATTERNS or use --db-patterns.")
        return

    if args.max_db_files:
        db_paths = db_paths[: args.max_db_files]

    print(f"Found {len(db_paths)} database file(s) to process.")
    total_ip_counts: Counter = Counter()

    for db_path in db_paths:
        print(f"Processing {db_path}")
        total_ip_counts.update(extract_ips_from_db(db_path, query=args.query))

    if not total_ip_counts:
        print("No IP addresses were extracted from the configured databases.")
        return

    write_ip_counts(total_ip_counts, args.output)
    print(f"Aggregated IP counts written to {args.output}")

    if args.abuse_key:
        abuse_ipdb_enrich(
            input_file=args.output,
            output_file=args.abuse_output,
            api_key=args.abuse_key,
            min_count=args.min_abuse_count,
            max_queries=args.max_abuse_queries,
        )


if __name__ == "__main__":
    main()
