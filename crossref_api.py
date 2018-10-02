#!/usr/bin/env python
'''
A self-contained means of testing queries for the CrossRef API.
You will need to edit this program with the query you want to run.

Usage:
    python crossref_api.py

Requirements:
    habanero
'''

import pprint

from habanero import Crossref


def main():
    '''
    The Crossref works function has many options
    ids         List of DOIs or other identifiers
    query       A query string
    filter      Filter options. Accepts a dict with filter names and their
                values. For repeating filter names, pass in a list of values
                to that filter name.
    offset      Number of records to start at, from 1 to 10,000.
    limit       Number of results to return. Default: 20. Max: 1000.
    sample      Number of random results to return. If you use sample, limit
                and offset will be ignored. Max: 100.
    sort        Field to sort on. If call includes a query, sort order will be
                relevance score. If not, will be DOI update date.
    order       Sort order ('asc' or 'desc')
    facet       Set to 'true' to include facet results (default: false).
                Optionally, pass a query string e.g. `facet=type-name:*`
    select      Select a subset of elements to return.
    cursor      Cursor character string to do paging. Default is None. Pass in
                '*' to do deep paging. Not all routes support cursors.
    cursor_max  Max records to retrieve. Only used when cursor param is used.
    '''

    cr = Crossref()

    options = {'ids': None,
               'query': None,
               'query_title': None,
               'query_container_title': None,
               'query_author': None,
               'query_editor': None,
               'query_chair': None,
               'query_translator': None,
               'query_contributor': None,
               'query_bibliographic': None,
               'query_affiliation': 'Univ Florida',
               'filters': None,
               'offset': None,
               'limit': None,
               'sample': 2,
               'sort': None,
               'order': None,
               'facet': None,
               'select': None,
               'cursor': None,
               'cursor_max': None}

    kwargs = {}
    for key, value in options.items():
        if value:
            kwargs[key] = value

    x = cr.works(**kwargs)

    print(x['message']['total-results'])
    # pprint.pprint(x['message']['items'])

if __name__ == '__main__':
    main()
