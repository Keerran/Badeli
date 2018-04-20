from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
# Create your views here.
from .models import *
from riotwatcher import RiotWatcher

from riotwatcher import RiotWatcher

def index(request):
	watcher = RiotWatcher('RGAPI-1adb2016-809b-4d86-b836-661eedceae00')

	my_region = 'EUW1'
	locale = 'en_US'
	version=None
	me = watcher.summoner.by_name(my_region, 'neroso')
	tags='all'
	print(me)

	# all objects are returned (by default) as a dict
	# lets see if i got diamond yet (i probably didnt)

	# Lets some champions
	static_champ_list = watcher.static_data.champions(my_region, locale, version, tags)
	static_champ_list_STR = str(static_champ_list)
	return HttpResponse(static_champ_list_STR)
