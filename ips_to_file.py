import sqlite3
import re
import pandas as pd
import csv

def ips_to_file():
    """
    Purpose: This function pareses through the the ubiquiti database logs and finds all instances
                of IP's withing the file.

    """

    print('Starting')
    connection_string = "\\\\DISKSTATION\\DataStore\\Logs\\3RDAVE\\SYNOSYSLOGDB_3RDAVE - Copy.DB"
    #connection_string = "\\\\DISKSTATION\\DataStore\\Logs\\3RDAVE\\2023-10-17_2023-11-16-Copy.DB"
    #connection_string = "\\\\DISKSTATION\\DataStore\\Logs\\3RDAVE\\bak_SYNOSYSLOGDB_3RDAVE.DB"
    count = 0
    ipv4_regex = "\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b"
    #file1 = open("d:\\RouterLogs\\IPs.csv", "w")
    field_names = ['ip','count']
    query = "SELECT * FROM logs LIMIT 50000" 

    IP_dict = {}
    #print(IP_dict)
    IPignorelist = ['127.0.0.1','99.145.235.143','127.0.0.1','8.8.8.8','8.8.4.4','1.1.1.1']

    print(query)
    print(connection_string)

    try:
        con = sqlite3.connect(connection_string)
        con.text_factory = lambda b: b.decode(errors='ignore')

        print('connected')
        cur = con.cursor()
        res = cur.execute(query)
        res = cur.fetchall()

        for rec in res:
            #if count > 1000:
            #    break
            found = re.findall(ipv4_regex,rec[13])
            #print("found :: {}".format(found))

            for val in found:
   
                #dictionary
                if val [:2] == '10' or val[:10] == "192.168.1." or val in IPignorelist:
                    #print(val)
                    continue

                elif val not in IP_dict.keys():
                    IP_dict.update({"{}".format(val):"1"})

                else:
                    ip_cnt = int(IP_dict.get("{}".format(val))) + 1
                    IP_dict[val]= ip_cnt

            count = count + 1

        with open("d:\\RouterLogs\\IPs.csv", "w", newline='') as csv_file:  
            writer = csv.DictWriter(csv_file,fieldnames=field_names)
            writer.writeheader()    
            #writer.writerows(IP_dict) 
            
            for key, value in IP_dict.items():
                writer.writerow([key, value])
            

        csv_file.close()
        print(count)
    except Exception as e:
        print("Error :: {}".format(e))


ips_to_file()