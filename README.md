# USQL to Excel

Simple exporter to export USQL queries as Excel workbooks.

## Setup

1. Install python requirements using

    python -m pip -r requirements.txt

2. Edit `config.yaml`

Start by copying `_config.yaml` template to config.yaml

- Set Dynatrace environment values (url, apiToken). API token with UserSession query is required.
- Set workbook name
- Define queries in the usqls array. Enter USQL query, name (Worksheet name), startTimestamep

## Run exporter

Just execute the script to produce XLSX workbook
    
    python usql2excel.py
