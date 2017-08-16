#!/usr/bin/python

import requests
import json

token_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
token_data = {
  "grant_type": 'client_credentials',
  "resource": 'https://management.core.windows.net/',
  "client_id": 'Enter the client ID',
  "client_secret": 'Enter Client Secret',
}

token_res = requests.post('https://login.microsoftonline.com/<ENter the tenant ID>/oauth2/token?api-version=1.0', headers=token_headers, data=token_data)
print token_res.json()["access_token"]
