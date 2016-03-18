#Lobbying.ie Watch
A simple Python script to monitor a registry search on lobbying.ie via RSS and post a tweet via a Twitter account and/or a direct message to a Twitter account when new lobbying activity is registered.  The tweet and direct message both contain the name of the lobbying organisation/individual, the dates that span the activity and a Bit.ly shortened link to the full entry on [lobbying.ie](https://lobbying.ie).

##Instructions
You may need to install the Bitly API module.

```
(sudo) pip install bitly_api
```

Obtain your [Bitly username & API key](http://dev.bitly.com/authentication.html).

You may need to install the Tweepy module.

```
(sudo) pip install tweepy
```

You can use the authentication credentials from an existing Twitter app or create a new one to obtain the consumer key, consumer secret, access token and access token secret in the [Twitter App management console](https://apps.twitter.com).

Add your search term(s), bit.ly username and password along with your key, secrets and access token as obtained above where indicated in the lobbywatch.py file.

Finally run 

```
python lobbywatch.py
```

If all works as expected you may then configure cron or some other scheduling mechanism to run the script at your required interval.

for example, the following cron entry would run the script twice per day, once at 10am and again at 4pm

```
0 10,16 * * * /usr/bin/python /path/to/lobbywatch.py
```