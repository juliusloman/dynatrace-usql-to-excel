import logging
import requests
import json
import xlsxwriter
import yaml


with open("config.yaml") as enviromentConfig:
    config = yaml.safe_load(enviromentConfig)


logger = logging.getLogger(__name__)
logging.basicConfig(level=config.get("loglevel",logging.INFO))

dtApiToken = config.get("environment").get("apiToken")
dtEnvironment = config.get("environment").get("url")
dtCertVerify = config.get("environment").get("certVerify", "true").lower() == "true"

workbook = xlsxwriter.Workbook(config.get("workbook"))

for usqlQuery in config["usqls"]:
    logger.info(f"Process query {usqlQuery.get('name')}")
    query = usqlQuery["query"]
    pageSize = usqlQuery["pageSize"]    
    startTimestamp = usqlQuery["startTimestamp"]
    worksheet = workbook.add_worksheet(usqlQuery.get("name"))
    row = 0
    pageOffset=0
    shouldRun = True

    while shouldRun:
        response = requests.get(f"{dtEnvironment}/api/v1/userSessionQueryLanguage/table", 
                            params={
                                "query": query,
                                "pageSize": pageSize,
                                "pageOffset": pageOffset,
                                "startTimestamp": startTimestamp
                            },
                            headers={"Authorization": f"api-token {dtApiToken}"}, 
                            verify=dtCertVerify)
        
        if response.status_code==200:        
            usqlResponse = response.json()            
            logger.debug(f"USQL returned {len(usqlResponse.get('values'))} values")

            if (pageOffset==0):
                worksheet.write_row(row=row, col=0, data=usqlResponse.get("columnNames"))
                row = row + 1

            for dataRow in usqlResponse.get("values"):
                worksheet.write_row(row=row, col=0, data=dataRow)
                row = row + 1    

            if (len(usqlResponse.get("values"))<pageSize):
                shouldRun = False
            else:
                pageOffset = pageOffset + pageSize
        else:
            logger.error(f"USQL Error {response.status_code} {response.text}")

workbook.close()