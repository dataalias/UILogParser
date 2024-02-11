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
    connection_string = "\\\\DISKSTATION\\DataStore\\Logs\\3RDAVE\\2023-10-17_2023-11-16-Copy.DB"
    count = 0
    ipv4_regex = "\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b"
    file1 = open("d:\\RouterLogs\\IPs.csv", "w")
    L = "id, host, ip, fac, prio, llevel, tag, utcsec, r_utcsec, tzoffset, ldate, ltime, prog, msg, msg_ip\r"
    query = "SELECT * FROM logs " \
        "where [r_utcsec] > 1702397594 " \
        "and [msg] like '%DST=%' " \
        "and [msg] like '%SRC=%' "
    query = "SELECT * FROM logs " 
    IP_list = []

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
            #if count > 10000:
            #    break
            #print('steppin')
            #print(str(rec[1]))
            #rec.msg = "\"" + rec.msg + "\""

            
            #msg_ip = re.findall(ipv4_regex,rec.msg)

            #id, host, ip, fac, prio, llevel, tag, utcsec, r_utcsec, tzoffset, ldate, ltime, prog, msg = rec

            #print(rec[13])
            #src_pos = rec[13].find('SRC=')
            #dst_pos = rec[13].find('DST=')
            #len_pos = rec[13].find('LEN=')
            #print("The src position is:{} and the dest position is:{}".format(src_pos, dst_pos))
            #src_ip = rec[13][src_pos+4:dst_pos-1]
            #dst_ip = rec[13][dst_pos+4:len_pos-1]
            #print('src_ip: ', src_ip, 'dst_ip:', dst_ip)

            found = re.findall(ipv4_regex,rec[13])

            for val in found:
                if val not in IP_list:
                    IP_list.append(val)
                    #print(val)



            #file1.writelines(str(rec))
            #file1.writelines('\n')

            count = count + 1
        IP_list.sort()
        print(IP_list)
        for IP in IP_list:
            file1.writelines(str(IP))    
            file1.writelines('\n')
        file1.close()
        print(count)
    except Exception as e:
        print("Error connecting to db: {}".format(e))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
