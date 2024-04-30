import requests
import json
import csv
import pandas as pd

def abuse_scroing(file_name):

    count = 0
    break_count = 100
    hit_count = 8

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
    #field_names= #['IP','COUNT','ABUSE_SCORE','countryCode','domain','isp','totalReports']
    field_names=['ip','count','abuseConfidenceScore','countryCode','domain','hostnames','ipAddress','ipVersion','isPublic','isTor','isWhitelisted','isp','lastReportedAt','numDistinctUsers','totalReports','usageType']

    output_file_name = file_name.replace('.csv','_output.csv')

    input_file = open(file_name, "r", newline='')
    output_file = open (output_file_name, "w", newline='')

    writer = csv.DictWriter(output_file,fieldnames=field_names)
    writer.writeheader()

    with open(file_name, "r", newline='') as input_file:
        dict_reader = csv.DictReader(input_file)
        list_of_dict = list(dict_reader)
        for dict in list_of_dict:
            if count > break_count:
                break
            cur_ip_addr = dict['ip']
            my_query = querystring
            my_query['ipAddress']=cur_ip_addr
            if int(dict['count'])>= hit_count:
                response = requests.request(method='GET', url=url, headers=headers, params=my_query)
                decodedResponse = json.loads(response.text)
                decodedResponse['data'].pop('hostnames')
                decodedResponse['data'].update(dict)
                writer.writerow(decodedResponse['data'])
                count = count + 1

    input_file.close()
    output_file.close()

file_name = "d:\\RouterLogs\\IPs.csv"
abuse_scroing(file_name)