# Monitor gCode Updates

## Purpose
CMS has will release changes to the gCodes for appropriate use criteria reporting. In order to maintain them in an EMR, I created this python script to send me an email alert when there are additions or deletions

## How Does it Work
CMS post the list of gCodes as an HTML table. This program uses Pandas to parse an HTTP response for that HTML table. Their is a csv file with the gCode data from a previous run of the script which is imported as another Pandas dataframe and the two are compared.\
If there are any additions or deletions, they are formatted as an HTML string and returned by the gCode_scraper script. The latest dataframe is then stored as the csv file for use with the next comparison.\
I created email_me as a script I might reuse for future projects. It is tied to a dummy gmail account and only requires 3 basic parameters to send an email. runDaily.py is a driver program.\
The driver program is scheduled as a task on my computer to run each day.

### About
I'm a software development student and this is my first program that is actually of any real use to me. It may not be the best way to do things, this was my first time using pandas, logging and other python features. My goal is to further refine these scripts to make other automations.