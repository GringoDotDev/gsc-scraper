#!/usr/bin/env python
"""
@author:    Jean-Christophe Chouinard. 
@role:      Sr. SEO Specialist at SEEK.com.au
@website:   jcchouinard.com
@LinkedIn:  linkedin.com/in/jeanchristophechouinard/ 
@Twitter:   twitter.com/@ChouinardJC

Learn Python for SEO
jcchouinard.com/python-for-seo

Get API Keys
jcchouinard.com/how-to-get-google-search-console-api-keys/

How to format your request
jcchouinard.com/what-is-google-search-console-api/
"""
# Standard library imports
from time import sleep
import pandas as pd

# Third party modules imports
from collections import defaultdict
import datetime
from dateutil import relativedelta

# Local modules imports
from date_manip import date_to_str
from oauth import authorize_creds, execute_request

"""
Initialize default end_date. Set 3 days in the past.
GSC doesn't allow more recent dates.
This'll be used when end_date is not defined.
"""
today = datetime.datetime.now()
days = relativedelta.relativedelta(days=3)
default_end = today - days


def gsc_by_url(
    webmasters_service, site, list_of_urls, creds, start_date, end_date=default_end
):
    """
    Extracts clicks and impressions from a list of URLs.
    """
    # Authorize credentials to log in the API
    # webmasters_service = authorize_creds(creds)

    # Make sure dates are in string format
    start_date = date_to_str(start_date)
    end_date = date_to_str(end_date)

    # Initialize empty dictionary
    scDict = defaultdict(list)
    i = 0
    n = len(list_of_urls)

    for url in list_of_urls:  # For each URL
        i += 1

        print(f"Fetching {url}, {i} of {n} ({round(i / n * 100, 1)}%)...")

        request = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensionFilterGroups": [
                {
                    "filters": [
                        {
                            "dimension": "page",  # page, query, country, device, searchAppearance
                            "operator": "equals",  # contains, equals, notEquals, notContains
                            "expression": url,
                        }
                    ]
                }
            ],
        }

        # make sure to retry in the case of an error (likely a rate limit)
        while True:
            try:
                response = execute_request(webmasters_service, site, request)
                # execute at most one request per second
                # helps with rate limits
                sleep(1)
            except:
                print("Hit rate limit, waiting...")
                # wait 20 minutes then try again
                sleep(60 * 20)
                continue
            break

        # Convert JSON to a dictionary
        scDict["page"].append(url)
        try:
            for row in response["rows"]:
                scDict["clicks"].append(row["clicks"] or 0)
                scDict["impressions"].append(row["impressions"] or 0)
        except Exception as e:
            print(f"An error occurred while extracting {url}: {e}")

    # Convert dictionary to a dataframe
    df = pd.DataFrame(data=scDict)
    return df
