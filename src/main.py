# This is a sample Python script.
import sqlite3
import re
import pandas as pd
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print('Starting')
    connection_string = "\\\\DISKSTATION\\DataStore\\Logs\\3RDAVE\\SYNOSYSLOGDB_3RDAVE.DB"
    connection_string = "\\\\DISKSTATION\\DataStore\\Logs\\3RDAVE\\2024-08-04_2024-09-03.DB"
    count = 0
    file1 = open("d:\\RouterLogs\\IPLogs.csv", "w")

    L = "id, host, ip, fac, prio, llevel, tag, utcsec, r_utcsec, tzoffset, ldate, ltime, prog, msg, msg_ip\r"

    query = "SELECT * FROM logs " \
        "where [r_utcsec] > 1702397594 " \
        "and [msg] like '%DST=%' " \
        "and [msg] like '%SRC=%' "
    query = "SELECT * FROM logs " 

    print(query)
    print(connection_string)

    try:
        con = sqlite3.connect(connection_string)
        con.text_factory = lambda b: b.decode(errors='ignore')

        print('connected')
        cur = con.cursor()

        #cur.execute("SELECT name FROM sqlite_master")
        #res = cur.fetchone()
        #print(res)

        res = cur.execute(query)
        
        #df=pd.DataFrame(cur.fetchall())
        res = cur.fetchall()
        file1.writelines(L)

        #for index, rec in df.iterrows():
        for rec in res:
  
            file1.writelines(str(rec))
            file1.writelines('\n')

    except Exception as e:
        print("Error connecting to db: {}".format(e))



