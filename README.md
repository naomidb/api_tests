# API Tests

There are four API tests here. The programs are mostly self-contained means of checking the response from various APIs to queries.
All of these programs require the user to edit the query in the program *before* running.

## VIVO API
`python vivo_api.py (-q | -i | -d) <config_file>`

You can run this with a query, insert, or delete flag. It requires a config file.

### Config requirements
vivo_email: Email address for VIVO account with query/update access
vivo_password: Password for said account
u_endpoint: Endpoint for update api
q_endpoint: Endpoint for query api

## WOS API
`python wos_api.py <config_file>`

Requires a config file.

### Config requirements
wos_credentials: "Username:Password" encoded in base 64

## PubMed API
`python pubmed_api.py <config_file>`

Requires a config file.

### Config requirements
pm_email: Email address to link to PubMed queries (inc ase you are warned of future throttling)

## CrossRef API
`python crossref_api.py`

Does not require a config file.
