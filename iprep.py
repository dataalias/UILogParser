import requests
import json
import csv
import pandas as pd

def abuse_scroing(file_name):

    # Defining the api-endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': '<<IPADDR>>',
        'maxAgeInDays': '90'
    }

    headers = {
        'Accept': 'application/json',
        'Key': '15d2eb74e34443f1781f9466437f336d7a70b6cb354e41cf9b85cbbe4521049b05891b9165641d6f'
    }
    field_names= ['IP','COUNT','ABUSE_SCORE','countryCode','domain','isp','totalReports']

    output_file_name = file_name.replace('.csv','_output.csv')

    input_file = open(file_name, "r", newline='')
    output_file = open (output_file_name, "w", newline='')

    writer = csv.DictWriterwriter(output_file,fieldnames=field_names)
    writer.writeheader()

    with open(file_name, "r", newline='') as input_file:
        reader = csv.reader(input_file)
        row1 = next(reader)  # gets the first line
        for row in reader:
            print(row)
            cur_ip_addr = row[0]
            print(cur_ip_addr)
            my_query = querystring
            my_query['ipAddress']=cur_ip_addr

            response = requests.request(method='GET', url=url, headers=headers, params=my_query)
            decodedResponse = json.loads(response.text)
            print (json.dumps(decodedResponse, sort_keys=True, indent=4))
            writer.writerow()
    input_file.close()
    output_file.close()

file_name = "d:\\RouterLogs\\IPs.csv"
abuse_scroing(file_name)