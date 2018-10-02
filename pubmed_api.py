#!/usr/bin/env python

'''
A self-contained means of testing queries for the PubMed API.
You will need to edit this program with the query you want to run.

Usage:
    python pubmed_api.py <config_file>

Requirements:
    PyYAML
    Entrez

'''

import pprint
import sys
import requests
from time import localtime, strftime

from Bio import Entrez
import yaml

class Citation(object):
    def __init__(self, data):
        self.data = data

    def check_key(self, paths, data=None):
        if not data:
            data = self.data
        if paths[0] in data:
            trail = data[paths[0]]
            if len(paths) > 1:
                trail = self.check_key(paths[1:], trail)
            return trail
        else:
            return ""

def get_config(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read())
    except:
        print("Error: Check config file")
        exit()
    return config

def get_ids(query, email):
    retstart = 0
    count_up = 0

    Entrez.email = email
    res = Entrez.esearch(term=query,
                         db='pubmed',
                         retmax=100000,
                         retstart=retstart)
    result = Entrez.read(res)
    id_list = result['IdList'] #pull relavent IDs from query
    total = result['Count']

    count_up += 100000
    if count_up < int(total): #if the number of results exceeds 100,000, you will need to run the query again
        retstart += 100000
        id_list += get_id_list(term)

    return id_list

def get_details(id_list, email):
    ids = ','.join(id_list)
    Entrez.email = email
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)

    return results

def main(config_path):
    config = get_config(config_path)
    email = config.get('pubmed_email')

    # Write your query here
    query = 'University of Florida[Affiliation] AND "last 1 days"[edat]'
    id_list = get_ids(query, email)
    results = get_details(id_list, email)

    print(results)

if __name__ == '__main__':
    main(sys.argv[1])
