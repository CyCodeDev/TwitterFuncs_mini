# This file must be imported
import requests
import json
import base64
import urllib.request as url
import urllib.parse
import numpy as np

#import oauth2 as oauth
#from requests_oauthlib import OAuth2Session


class cytweet: #Twitter API requires that a user use base 64 with a series of concatenation
	def __init__(self, consumer_key, consumer_secret): #, access_token, access_token_secret):
		self.rfc = consumer_key +':'+ consumer_secret
		self.creds = base64.b64encode(self.rfc.encode('utf-8')).decode()
		self.token = 1
# Retrieve a token		
	def getToken(self):
		tokenURL = 'https://api.twitter.com/oauth2/token'
		tokenHeader = {'User-Agent': 'Python request', 'Authorization': 'Basic '+ self.creds, 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Content-Length': '29', 'Accept-Encoding': 'gzip'}
		self.token = requests.request('POST', tokenURL, headers=tokenHeader, data='grant_type=client_credentials', stream=False).json()['access_token']
		return self.token

#If you are using the 30-day endpoint:
#https://api.twitter.com/1.1/tweets/search/30day/my_env_name.json
#If you are using the full-archive endpoint:
#https://api.twitter.com/1.1/tweets/search/fullarchive/my_env_name.json

# Begin first search method
	def tSearch(self, token, searchTerm, dateFrom, dateTo, next):
		#payload = {"query": "@profile OR #hashtag OR to:toProfile lang:en -(from:fromProfile)", "fromDate": "201805220000", "toDate": "201806210000"}
		self.payload = {"query": searchTerm, "fromDate": dateFrom, "toDate": dateTo, "next": next}
		endpoint = 'https://api.twitter.com/1.1/tweets/search/fullarchive/FullArchive.json'
		main_header = {'User-Agent': 'Python request', 'Authorization': 'Bearer ' + token, 'Accept-Encoding': 'gzip'}
		self.results = requests.request('GET', endpoint, headers=main_header, params=self.payload, data=None)
		return self.results.json()

# Checks if there is any additional page of search data
	def continueTSearch(self, token, searchTerm, dateFrom, dateTo, next=None):
		#payload = {"query": "@profile OR #hashtag OR to:toProfile lang:en -(from:fromProfile)", "fromDate": "201805220000", "toDate": "201806210000"}
		nextEncode = urllib.parse.quote_plus(next)
		self.payload = {"query": searchTerm, "fromDate": dateFrom, "toDate": dateTo, "next": nextEncode}
		endpoint = 'https://api.twitter.com/1.1/tweets/search/30day/SandboxProd.json'
		main_header = {'User-Agent': 'Python request', 'Authorization': 'Bearer ' + token, 'Accept-Encoding': 'gzip'}
		self.results = requests.request('GET', endpoint, headers=main_header, params=self.payload, data=None)
		return self.results.json()
