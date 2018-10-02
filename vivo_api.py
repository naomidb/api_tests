'''
A self-contained means of testing queries for the VIVO API.
You will need to edit this program with the query you want to run.

Usage:
    python vivo_api.py (-q | -i | -d) <config_file>

Options:
    -q      Use the query endpoint
    -i      Use the update endpoint to insert (requires an account with admin rights)
    -d      Use the update endpoint to delete (requires an account with admin rights)
'''

import requests
import sys
import yaml

def get_config(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read())
    except:
        print("Error: Check config file")
        exit()
    return config

def do_query(payload, endpoint):
    print("Query:\n:" + payload['query'])
    headers = {'Accept': 'application/sparql-results+json'}
    response = requests.get(endpoint2, params=payload, headers=headers, verify=False)
    print(response)
    print(response.json())
    return response

def do_update(payload, endpoint):
    print("Query:\n:" + payload['query'])
    response = requests.post(endpoint, params=payload, verify=False)
    print(response)
    return response

def main(q_type, config_path):
    config = get_config(config_path)
    email = config.get('vivo_email')
    password = config.get('vivo_password')

    if q_type == '-i':
        endpoint = config.get('u_endpoint')
        # Write insert query below
        query = """
                INSERT DATA {
                    GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2> {

                    }
                }
                """
    elif q_type == '-d':
        endpoint = config.get('u_endpoint')
        # Write delete query below
        query = """
                DELETE DATA {
                    GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2> {
                    
                    }
                }
                """
    elif q_type == '-q':
        endpoint = config.get('q_endpoint')
        # Write query below
        query = """
                SELECT
                WHERE{

                }
                """
    else:
        print("Incorrect flag.")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])