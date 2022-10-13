#!/usr/bin/env python
import datetime

import pandas as pd

from gsc_by_url import gsc_by_url
from oauth import authorize_creds

import sys

start_index = 0
count = None

try:
    start_index = int(sys.argv[1])
    count = int(sys.argv[2])
except:
    pass

site = "https://www.carvana.com"

# you get this from gsc
creds = "client_secrets.json"

# pull 365 days of data
start_date = datetime.datetime.now() - datetime.timedelta(days=365)

search_console = authorize_creds(creds)

# supposedly pandas can read 100 GB into memory at a time so not overly worried
df = pd.read_csv("input.csv")

if count == None:
    count = len(df)

list_of_urls = df["URL"][start_index : start_index + count]

args = search_console, site, list_of_urls, creds, start_date
out = gsc_by_url(*args)
out_df = pd.DataFrame(out)
out_df.to_csv(
    path_or_buf=f"output.csv",
    header=False,
    index=False,
    mode="a+",
)
