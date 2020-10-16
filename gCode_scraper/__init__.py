import requests
import pandas as pd
import logging
import functools
import os
from pathlib import Path
from email.mime.text import MIMEText


def createNewDf():
    """ 
    Reads in HTML table from website. 
    returns Pandas dataframe of latest table
    """
    url = 'https://www.cms.gov/Medicare/Quality-Initiatives-Patient-Assessment-Instruments/Appropriate-Use-Criteria-Program/CDSM'
    page = requests.get(url)
    return pd.read_html(page.content)[0]


def compareData(newDf):
    """ 
    Takes in today's dataframe
    returns a dictionary of the additions and deletions 
    """
    try:
        sourcePath = Path(r'./gCode_scraper/source/codes.csv')
        oldDf = pd.read_csv(sourcePath)
    except pd.errors.EmptyDataError: 
        logging.warning('Prior record not found, saving todays record.')
        return {'additions': newDf, 'deletions': newDf.iloc[0:0]}
    finally: 
        newDf.to_csv(sourcePath, index=False, header=True)

    # Merge data frames and store additions and deletions
    mergedDf = oldDf.merge(newDf, indicator=True, how='outer')
    additions = mergedDf[['Mechanism Name', 'Code']
                         ][mergedDf['_merge'] == 'right_only']
    deletions = mergedDf[['Mechanism Name', 'Code']
                         ][mergedDf['_merge'] == 'left_only']
    return {'additions': additions, 'deletions': deletions}


def handleResults(resultDict):
    """ Logs out the results for reference and sends email """
    changes = [] 
    # Handle additions
    if(not resultDict['additions'].empty):
        logging.info('\n***ADDITIONS***\n%s',
                     resultDict['additions'].to_string(header=False, index=False))
        # convert df to html string with label
        changes.append('<p><b>Additions</b></p> %s' %
                       resultDict['additions'].to_html(index=False))
    else:
        logging.info("No additions")
    # Handle Deletions
    if(not resultDict['deletions'].empty):
        logging.info('\n***Deletions***\n%s',
                     resultDict['deletions'].to_string(header=False, index=False))
        # convert df to html string with label
        changes.append('<p><b>Deletions</b></p> %s' %
                       resultDict['deletions'].to_html(index=False))
    else:
        logging.info("No deletions")
    return '<br>'.join(changes) # create single string


def run():
    logging.basicConfig(filename='./gCode_scraper/gCode_scraper.log',
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)

    df = createNewDf()
    result = compareData(df)
    emailMessage = handleResults(result)
    # only return value if there was changes. This prevents empty email
    if len(emailMessage) > 0:
        return emailMessage


if(__name__ == '__main__'):
    run()
