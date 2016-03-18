#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import urllib
import os
import xml.dom.minidom
import bitly_api
import re

#Your lobbying search term(s)
query = ''
#change to 1 if you would like to publicly tweet using the twitter app you have configured below when new lobbying activity is detected
tweetit = 0
#Your Twitter consumer key
consumer_key = ''
#Your Twitter consumer secret
consumer_secret = ''
#Your Twitter access token
token_key = ''
#Your Twitter access token secret
token_secret = ''
#The twitter account you would like to direct message when new activity is detected
#e.g. @example without the '@'
#Leave empty if you do not wish to direct message new activity
dmTwitterAccount = ''
#Your bit.ly username
bitlyUser = ''
#Your bit.ly password
bitlyPass = ''


#No need to edit beyond this point
feedurl = 'https://www.lobbying.ie/api/ExportReturns/Rss/Search?currentPage=1&pageSize=200&queryText=' + urllib.urlencode(query) + '&subjectMatters=&subjectMatterAreas=&period=&returnDateFrom=&returnDateTo=&lobbyist=&lobbyistId=&dpo=&publicBodys=&jobTitles=&client='
datafile = 'data.dat'
#The description elements of the lobbying.ie RSS feeds contain HTML, this is used to remove it
rep = {"<p>": "", "</p>": "\n", "<strong>": "", "</strong>": "", "From ": "", "to": "-", "Public policy area": "Policy Area"}

print 'Starting script'
message = 'No new lobbying'
response = urllib.urlopen(feedurl)
feed = xml.dom.minidom.parse(response)
channel = feed.getElementsByTagName('channel')[0]
item = channel.getElementsByTagName('item')[0]
guid = None
print 'Checking data file..'
if os.path.isfile(datafile):
  print 'We have an existing data file'
  with open(datafile,'r') as f:
    guid = f.readline()
if guid != item.getElementsByTagName('guid')[0].firstChild.data:
  #we have a new lobby item
  url = item.getElementsByTagName('link')[0].firstChild.data
  description = item.getElementsByTagName('description')[0].firstChild.data
  rep = dict((re.escape(k), v) for k, v in rep.iteritems())
  pattern = re.compile("|".join(rep.keys()))
  description = pattern.sub(lambda m: rep[re.escape(m.group(0))], description)
  dlist = description.split('\n')
  message = "New " + query + " lobbying registered:\n\n" + dlist[0] + '\n' + dlist[1] + '\n' + dlist[3]
  c = bitly_api.Connection(bitlyUser,bitlyPass)
  surl = c.shorten(url)['url']
  message = message + "\n\n" + surl
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(token_key, token_secret)
  api = tweepy.API(auth)
  if tweetit == 1:
    try:
      api.update_status(message)
      print 'Tweet posted :)'
    except tweepy.error.TweepError, e:
      print 'There was a problem posting the tweet'
      myErr = e.message[0]['message']
      print myErr
      if dmTwitterAccount != '':
        api.send_direct_message(screen_name=dmTwitterAccount,text='IU ERROR:' + str(myErr) + message)
  print message
  with os.fdopen(os.open(datafile,os.O_WRONLY|os.O_CREAT, 0777),'w') as f:
    f.write(item.getElementsByTagName('guid')[0].firstChild.data)
    print 'GUID saved'
  if dmTwitterAccount != '':
    api.send_direct_message(screen_name='freelancewebdev',text=message)
else:
  print message
