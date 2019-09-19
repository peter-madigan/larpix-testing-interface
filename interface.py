'''
Here is some example code demonstrating how to query the larpix-testing
database and upload results

You can customize the default settings by setting these evironment variables:
  LARPIX_DB_BASE_URL : url that points the the larpix db base (stored in interface.base_url)
  LARPIX_USER : default user to authenticate with (stored in interface.user)

The interface is relatively simple::

  response, model_urls = interface.get()
  model_urls.keys() # database model names
  asic_url = model_url['asic'] # url to access 'asic' model functions
  response, content = interface.get(asic_url)
  print(content['count']) # available 'asic's from query
  print(content['results']) # description of 'asic's in query
  response, content = interface.post(asic_url, data={'version': 1}) # create new 'asic' in database

  response, content = interface.get(asic_url)
  asic_id = print(content['results'][0]['pk']) # id associated with 'asic'
  asic0_url = content['results'][0]['url']
  response, content = interface.get(asic0_url) # get info about specific asic
  response, content = interface.patch(asic0_url, data={'version': 2}) # update 'asic' entry

'''


import requests
from getpass import getpass
from urllib.parse import urljoin

import os
from functools import wraps

base_url = 'http://192.168.99.100/larpix_testing_db/'
if 'LARPIX_DB_BASE_URL' in os.environ:
    base_url = os.environ['LARPIX_DB_BASE_URL']

user = 'larpix'
if 'LARPIX_DB_USER' in os.environ:
    user = os.environ['LARPIX_DB_USER']

## Basic helper functions for handling http requests and parsing
def add_trailing_slash(f):
    @wraps(f)
    def added_trailing_slash(url, *args, **kwargs):
        if url[-1] != '/':
            url += '/'
        return f(url, *args, **kwargs)

# Get entries in database
@add_trailing_slash
def get(url=base_url, username=user):
    result = requests.get(url, auth=(username, getpass()))
    print(result)
    if not result.status_code == 200:
        return result, {}
    return result, result.json()

# Create new entry in database
@add_trailing_slash
def post(url=base_url, data=None, username=user):
    if data is None:
        data = {}
    result = requests.post(url, data=data, auth=(username, getpass()))
    print(result)
    if not result.status_code == 200:
        return result, {}
    return result, result.json()

# Update entry in database
@add_trailing_slash
def patch(url=base_url, data=None, username=user):
    if data is None:
        data = {}
    result = requests.patch(url, data=data, auth=(username, getpass()))
    if not result.status_code == 200:
        return result, {}
    return result, result.json()

# Delete entry from database (USE WITH CAUTION)
@add_trailing_slash
def delete(url=base_url, username=user):
    result = requests.delete(url, auth=(username, getpass()))
    if not result.status_code == 200:
        return result, {}
    return result, result.json()

# Get info about database interface
@add_trailing_slash
def options(url=base_url, username=user):
    result = requests.options(url, auth=(username, getpass()))
    if not result.status_code == 200:
        return result, {}
    return result, result.json()
