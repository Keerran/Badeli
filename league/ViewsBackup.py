from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import TemplateView
from django.conf.urls import url
from django.contrib.auth import login, authenticate, logout 
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .static.python.RSA import generate, encrypt, decrypt
from .models import *
from requests import HTTPError
from .static.python.APIKey import APIKey
tiers = ["","bronze","silver","gold","platinum","diamond","master","challenger"]
# Create your views here.
class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html', context=None)
	def post(self, request, **kwargs):
		pass
def mySignup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			print(username)
			print(raw_password)
			user = authenticate(username=username, password=raw_password)
			print(user)
			login(request, user)
			return redirect('home')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})
def myLogout(request):
	logout(request)

	return redirect('home')
def set_password(self, UnsafePassword):
	pubKey = "2257, 47"
	encryptedPassword = (encrypt(UnsafePassword, pubKey))
	#uses RSA encryption to encrypt the password
	self.password = encryptedPassword

def myLogin(request):
	pubKey = "2257, 47"
	if request.method == 'POST':
		username = request.POST.get('username')
		raw_password = request.POST.get('psw')
		user = authenticate(username=username, password=raw_password)
		if user == None:
			return redirect('home')
		else:
			login(request, user)
		return redirect('home')

class app(TemplateView):
	template_name = 'app.html'
class mySearch(TemplateView):
	def displayStats(league, rank, tier, ratio, wins, losses, lp, hotStreak):
		league = league
		RankTier = str(tier).title() + ' ' + str(rank)
		LP = str(lp) + 'LP / '
		WinsLosses = str(wins) + 'W' +  ' ' +  str(losses) + 'L'
		WinRatio = 'Win Ratio ' + str(ratio)
		final = [league, RankTier, LP, WinsLosses, WinRatio, hotStreak]
		print(final)
		print("HELLO")
		return final

	def get(self, request, **kwargs):
		#return render(request, 'app.html', context =None)
	#def post(self, request, **kwargs):
		APIKeyValue = APIKey()
		key = RiotWatcher(APIKeyValue)
		region = 'euw1'
		myProfileIconURLBase = '//opgg-static.akamaized.net/images/profile_icons/profileIcon[x].jpg'
		summonerNameSearch = self.request.GET.get('summonerName')
		soloStatsDisplay = flexStatsDisplay = [""] * 6
		soloTier = flexTier = ""
		if Summoner.objects.filter(summoner_name = summonerNameSearch).count() > 0:
			print("Found")
			summoner = Summoner.objects.get(summoner_name = summonerNameSearch)
			mySummonerId = summoner.summonerID
			myProfileIconId = summoner.profileIconId
			summonerNameSearch = summoner.summoner_name
			
			myProfileIconURL = myProfileIconURLBase.replace('[x]', str(myProfileIconId))
			print(str(mySummonerId) + ' ' + str(myProfileIconId))

#I could of also stored this data in a table in my database but I am not due to hand restraints
		else:
			
			try:
				summoner = key.summoner.by_name(region, summonerNameSearch)
				myProfileIconId = summoner["profileIconId"]
				myProfileIconURL = myProfileIconURLBase.replace('[x]', str(myProfileIconId))
				mySummonerId = summoner["id"]
				summonerNameSearch = summoner["name"]

			except HTTPError as error:
				if error.response.status_code == 429:
				#Check documentation for explanations of error codes
					summoner = ('''An error has occured, due to too many requests have been made to the Riot API.  Please try again after '''.format(e.headers['Retry']) )
				elif error.response.status_code == 404:
					summoner = ('There is no summoner with that name on the region ' + region)
				return render(request, 'App.html', {
					'Summoner_Name' : summonerNameSearch, 'Profile_Image' : myProfileIconURL
					})

		try:
			rankedStats= key.league.positions_by_summoner(region, mySummonerId)
			print(rankedStats)
			flexStats = {}
			soloStats = {}
			for stats in rankedStats:
				if stats['queueType'] == "RANKED_SOLO_5x5":
					soloStats = stats
				elif stats['queueType'] == "RANKED_FLEX_SR":
					flexStats = stats

			if soloStats != {}:
				queueType = 'solo'
				soloTier = soloStats['tier']
				soloRank = soloStats['rank']
				soloLeagueName = soloStats['leagueName']
				soloLP = soloStats['leaguePoints']
				soloWins = soloStats['wins']
				soloLosses = soloStats['losses']
				soloStreak = soloStats['hotStreak']
				soloRatio = str(int(int(soloWins)/(int(soloLosses) + int(soloWins)) * 100)) + "%"
				soloStatsDisplay = mySearch.displayStats(soloLeagueName, soloRank, soloTier, soloRatio, soloWins, soloLosses, soloLP, soloStreak)
			if flexStats != {}:
				queueType = 'flex'
				flexTier = flexStats['tier']
				flexRank = flexStats['rank']
				flexLeagueName = flexStats['leagueName']
				flexLP = flexStats['leaguePoints']
				flexWins = flexStats['wins']
				flexLosses = flexStats['losses']
				flexStreak = flexStats['hotStreak']
				flexRatio = str(int(int(flexWins)/(int(flexLosses) + int(flexWins)) * 100)) + '%'
				flexStatsDisplay = mySearch.displayStats(flexLeagueName, flexRank, flexTier, flexRatio, flexWins, flexLosses, flexLP, flexStreak)
			


		except HTTPError as error:
			if error.response.status_code == 429:
			#Check documentation for explanations of error codes
				rankedStats = ('''An error has occured, due to too many requests have been made to the Riot API.  Please try again after '''.format(e.headers['Retry']) )
			elif error.response.status_code == 404:
				rankedStats = ('There is no summoner with that name on the region ' + region)
		highestTier = ""
		if flexStats == {} and soloStats == {}:
			return render(request, 'App.html',{'has_stats': False, 'Profile_Image' : myProfileIconURL, 'Summoner_Name': summonerNameSearch,})
		else:
			soloIndex = tiers.index(soloTier.lower())
			flexIndex = tiers.index(flexTier.lower())
			highestTier = tiers[max(soloIndex,flexIndex)]

			return render(request, 'App.html',{'has_stats': True,
			'Summoner_Name': summonerNameSearch,
			'Solo_League' : soloStatsDisplay[0], 'Solo_Rank_Tier' : soloStatsDisplay[1], 'Solo_LP' : soloStatsDisplay[2], 'Solo_Wins_Losses' : soloStatsDisplay[3], 'Solo_WR' : soloStatsDisplay[4],
			'Solo_Streak' : soloStatsDisplay[5],
			'Profile_Image' : myProfileIconURL,
			'flex_League' : flexStatsDisplay[0], 'flex_Rank_Tier' : flexStatsDisplay[1], 'flex_LP' : flexStatsDisplay[2], 'flex_Wins_Losses' : flexStatsDisplay[3], 'flex_WR' : flexStatsDisplay[4],
			'flex_Streak' : flexStatsDisplay[5],
			'highest_tier' : highestTier,
			})

			
"""
class TestPageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'Test.html', context=None)
# Create your views here.
 """  
