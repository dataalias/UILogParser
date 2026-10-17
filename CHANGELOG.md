# Changelog

## Unreleased

### Added
- `src/abuse_filter.py` with `get_abusive_ips`, which selects IPs from the abuse CSV with `abuseConfidenceScore >= 50` and `count > 100`.
- `abusive_ips_to_mongo_script`, which generates a mongo script that adds those IPs to the `DenyListIPAddresses` firewall group on the UDM Pro (validates IPs, prints a backup of the group, `$addToSet`, prints the result).
- README usage instructions, `CLAUDE.md`, and this changelog.

## Earlier
- IP extraction to file (`ips_to_file.py`), AbuseIPDB lookup (`iprep.py`), abuse list, and Mongo notes (`docs/Mongo.md`).
