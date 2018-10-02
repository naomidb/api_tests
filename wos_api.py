#!/usr/bin/env python

'''
A self-contained means of testing queries for the WOS API.
You will need to edit this program with the query you want to run.

Usage:
    python wos_api.py <config_file>

'''

import subprocess
import time
import requests

import yaml

WOK_SEARCH_URL = 'http://search.webofknowledge.com/esti/wokmws/ws/WokSearchLite'

class Template():
    search_template = '''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:woksearchlite="http://woksearchlite.v3.wokmws.thomsonreuters.com">
            <soapenv:Header/>
            <soapenv:Body>
            <woksearchlite:search>
                 <queryParameters>
                    <databaseId>{databaseId}</databaseId>
                    <userQuery>{userQuery}</userQuery>
                    <editions>
                    <collection>{collection}</collection>
                    <edition>SCI</edition>
                   </editions>
                   <editions>
                    <collection>{collection}</collection>
                    <edition>SSCI</edition>
                   </editions>
                   <editions>
                    <collection>{collection}</collection>
                    <edition>AHCI</edition>
                   </editions>
                   <editions>
                    <collection>{collection}</collection>
                    <edition>ESCI</edition>
                   </editions>
                    <timeSpan>
                        <begin>{begin}</begin>
                        <end>{end}</end>
                    </timeSpan>
                    <queryLanguage>{queryLanguage}</queryLanguage>
                 </queryParameters>
                 <retrieveParameters>
                    <firstRecord>{firstRecord}</firstRecord>
                    <count>{count}</count>
                 </retrieveParameters>     
            </woksearchlite:search>
            </soapenv:Body>
        </soapenv:Envelope>
    '''

def get_config(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read())
    except:
        print("Error: Check config file")
        exit()
    return config

def get_token(uf_credentials):
    curl_call = 'curl -H "Authorization: Basic' + uf_credentials + '" -d "@msg.xml" -X POST "http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate"'
    response = subprocess.check_output(curl_call, shell=True)
    print("Response: ", response)
    try:
        res = str(response)
        result = res[res.index("<return>")+len("<return>"):res.index("</return>")]
        print(result)
        token = result
    except ValueError as e:
        #wait for throttling to end
        print("Waiting 60 seconds for api")
        time.sleep(60)
        get_token()
    return token

def do_search(SID):
    params = {}
    # Modify the params below to create your search terms
    params['databaseId'] = 'WOS'
    params['collection'] = 'WOS'
    params['queryLanguage'] = 'en'
    params['userQuery'] = 'AD=(University Florida OR Univ Florida OR UFL OR UF)'
    params['begin'] = '2018-05-01'
    params['end'] = '2018-05-02'
    params['firstRecord'] = '1'
    params['count'] = '100'

    headers = {'Cookie': 'SID='+SID}
    data = Template.search_template.format(**params)
    print(data)
    result = requests.post(WOK_SEARCH_URL, data=data, headers=headers)
    print(result.text)
    print(find_parameter(result.text, 'queryId'))
    print(find_parameter(result.text, 'recordsFound'))
    print(find_parameter(result.text, 'recordsSearched'))

def find_parameter(body, param):
    try:
        start = '<' + param + '>';
        end = '</' + param + '>';
        startIndex = body.index(start)    
        endIndex = body.index(end)
        return body[startIndex:endIndex]
    except ValueError:
        return ""

def main(config_path):
    config = get_config(config_path)
    SID = get_token(config.get('uf_credentials'))

    do_search(SID)

if __name__ == '__main__':
    main(sys.argv[1])