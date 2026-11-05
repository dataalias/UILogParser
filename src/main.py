import sqlite3
from pathlib import Path


if __name__ == "__main__":
    print('Starting')
    log_folder = Path("\\\\DISKSTATION\\DataStore\\Logs\\3RDAVE")
    database_files = sorted(log_folder.glob("*.DB"))
    query = "SELECT * FROM logs"
    header = (
        "id, host, ip, fac, prio, llevel, tag, utcsec, r_utcsec, "
        "tzoffset, ldate, ltime, prog, msg, msg_ip\r"
    )

    print(query)
    print(f"Database folder: {log_folder}")

    if not database_files:
        print(f"No .DB files found in {log_folder}")
    else:
        for database_file in database_files:
            print(f"Found database: {database_file.name}")

        try:
            with open("d:\\RouterLogs\\IPLogs.csv", "w") as output_file:
                output_file.writelines(header)

                for database_file in database_files:
                    try:
                        with sqlite3.connect(database_file) as con:
                            con.text_factory = lambda b: b.decode(errors="ignore")
                            print(f"Connected to {database_file.name}")
                            records = con.execute(query).fetchall()

                        for record in records:
                            output_file.write(f"{record}\n")
                    except sqlite3.Error as error:
                        print(f"Error reading {database_file.name}: {error}")
        except OSError as error:
            print(f"Error opening output file: {error}")



