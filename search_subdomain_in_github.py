#!/bin/python

print '==| maded by: ahmed hamada |=='
print 'usage: cat subdomians.txt|python search_subdomain_in_github.py\n'

import requests
import json
import time
import sys

# == to solve == #

#1 limitation  - 30 requests per minute.
	# You have triggered an abuse detection mechanism. Please wait a few minutes before you try again
	# https://developer.github.com/v3/search/#rate-limit
	# tried use 6 tokens but it is 30 request per account
#2 extract github search links in arranged


tokens = ["a9648f67b142c5d54e1c31960ceb7aeeb881e83a","fadf1923fe98900d5ddf9f2884d97430b64fc720"]
current= -1

def get_arranged_one_token(tokens):
	global current
	if current ==1:
		current=-1
	current = current+1
	return tokens[current]

def padding(padding_space,before,value):
	print ' '*padding_space+before+str(value)

# line="\"wiki.admin.trello.com\"" # 2 results
#line="\"akoam.com\" \"sarhan2/xyz7/234.m3u8\""


x=1;
counter = 0
html_url=[]
time_start_point=int(time.time())


for line in sys.stdin:
	# print line
	counter = counter + 1
	line=line.rstrip()
	y= get_arranged_one_token(tokens)
	auth_header={"Authorization":"token "+y}
	# print y
	
	if counter % 52 == 0:
		print 'will sleep: '+str( (time_start_point+60) -time.time() )
		time.sleep( abs((time_start_point+60) -time.time()) )  #abs not best solution :)
		time_start_point=time.time() #reset the timer
	
	try:
		x=requests.get("https://api.github.com/search/code?per_page=100&type=Code&q=\""+line+"\"&page=1",headers=auth_header)
		dump=json.loads(x.text)
		total_count= dump['total_count']
		print "[" + str(total_count) + "]" + line

		#print uniq github link result
		for lol in dump['items']:
			if lol['html_url'] not in html_url:
				padding(5,'[*] ',lol['html_url'])
				html_url.append(lol['html_url'])
	except Exception as e:
		print '== failed =='
		print '[X]error: '+str(e)+dump['message']