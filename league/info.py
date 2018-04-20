from .models import *
from riotwatcher import RiotWatcher

from riotwatcher import RiotWatcher

watcher = RiotWatcher('RGAPI-482a55db-9abb-483d-a569-919b4cb70be1')

my_region = 'EUW1'

me = watcher.summoner.by_name(my_region, 'neroso')
print(me)

# all objects are returned (by default) as a dict
# lets see if i got diamond yet (i probably didnt)
my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
print(my_ranked_stats)

# Lets some champions
static_champ_list = watcher.static_data.champions(my_region)
print(static_champ_list)
"""
# Error checking requires importing HTTPError from requests

from requests import HTTPError

# For Riot's API, the 404 status code indicates that the requested data wasn't found and
# should be expected to occur in normal operation, as in the case of a an
# invalid summoner name, match ID, etc.
#
# The 429 status code indicates that the user has sent too many requests
# in a given amount of time ("rate limiting").

try:
    response = watcher.summoner.by_name(my_region, 'this_is_probably_not_anyones_summoner_name')
except HTTPError as err:
    if err.response.status_code == 429:
        print('We should retry in {} seconds.'.format(e.headers['Retry-After']))
        print('this retry-after is handled by default by the RiotWatcher library')
        print('future requests wait until the retry-after time passes')
    elif err.response.status_code == 404:
        print('Summoner with that ridiculous name not found.')
    else:
        raise
"""
