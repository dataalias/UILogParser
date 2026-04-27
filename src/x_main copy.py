# This is a sample Python script.
import sqlite3
import pyodbc 
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print('Starting')
    connection_string = "\\\\DISKSTATION\\DataStore\\Logs\\3RDAVE\\SYNOSYSLOGDB_3RDAVE.DB"
    connection_string = "\\\\DISKSTATION\\DataStore\\Logs\\3RDAVE\\SYNOSYSLOGDB_3RDAVE - Copy.DB"

    query = "SELECT * FROM logs " \
        "where [r_utcsec] > 1702397594 " \
        "and [msg] like '%DST=%' " \
        "and [msg] like '%SRC=%' "
    query = "SELECT * FROM logs limit 500" 

    print(query)
    print(connection_string)
    insert_query = "INSERT INTO Stage.Ubiquiti.RouterLogs values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    connection= 'DRIVER={ODBC Driver 18 for SQL Server};Server=RAGE/DEVRAGE;Database=Stage;Trusted_Connection=yes'
    connection= 'DRIVER={SQL Server Native Client 11.0};Server=RAGE/DEVRAGE,1433;Database=Stage;Trusted_Connection=yes'


    try:
        from_con = sqlite3.connect(connection_string)
        from_con.text_factory = lambda b: b.decode(errors='ignore')

        to_con = pyodbc.connect(connection)
        to_cur = to_con.cursor()

        print('connected')
        from_cur = from_con.cursor()
        from_cur.execute(query)
        to_cur.executemany(insert_query, from_cur.fetchall())        

    except Exception as e:
        print("Error connecting to db: {}".format(e))



