from django.views.generic import TemplateView
from django.contrib.auth import logout

from league.constants import queues, runes
from .forms import SignUpForm
from .models import *
from requests import HTTPError
from .static.python.APIKey import riot_key
import time
from .static.python.ChampWinRatios import champ_win_ratios

tiers = ["", "bronze", "silver", "gold", "platinum", "diamond", "master", "challenger"]


class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html', context=None)

	def post(self, request, **kwargs):
		pass


class Stats:
	def __init__(self, league, tier, lp, wins_losses, win_ratio, hot_streak):
		self.league = league
		self.tier = tier
		self.lp = lp
		self.winsLosses = wins_losses
		self.winRatio = win_ratio
		self.hotStreak = hot_streak


"""
This is the function that will be ran when the user enters the /signup/ page.
It will load up the SignUpForm in the forms.py file and then check if the user credentials are valid.
It will then authenticate the user(logging them into the website) and then save the information in the database.
"""


def badeli_signup(request):
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


"""
This function will be ran when the user presses the logout button, which will then use the built in django 
log out system to log them out
of the website and then redirect them to the home page.
"""


def badeli_logout(request):
	logout(request)
	return redirect('home')


def set_password(self, UnsafePassword):
	pub_key = "2257, 47"
	encrypted_password = (encrypt(UnsafePassword, pub_key))
	# uses RSA encryption to encrypt the password
	self.password = encrypted_password


def badeli_login(request):
	pubKey = "2257, 47"
	if request.method == 'POST':
		username = request.POST.get('username')
		raw_password = request.POST.get('psw')
		user = authenticate(username=username, password=raw_password)
		if user is None:
			return redirect('home')
		else:
			login(request, user)
		return redirect('home')


"""
This class is used to store the information of a given summoner name, which will be used in 
app.html to present their statistics such as
amount of ranked games won.
"""

"""
This is a class that will instantiated during run time and will become an object when instantiated.
It contains all the information that will be needed when displaying information from a specific 
match when a summoner's name has been searched.
It will contain it's on API calls, to the match endpoint, to get obtain that further information,
which will be sorted and saved as variables.
"""


class Participant:
	def __init__(self, account_id, summonerName, champion_id):
		pass


class Match:
	def __init__(self, gameInfo, accountID, summonerID, summoner_name, key):
		region = 'euw1'
		self.accountID = accountID
		summoner = cass.Summoner(account=accountID)
		self.summonerID = summonerID
		self.summonerName = summoner_name
		self.game = gameInfo
		self.player_stats = gameInfo.participants[summoner]
		self.timestamp = self.game.creation
		self.gameID = self.game.id
		# self.role = self.game.role
		# self.lane = self.game.lane
		self.championID = self.player_stats.champion.id
		# match = key.match.by_id(region, self.gameID)

		self.queueID = gameInfo.queue.id
		self.queueType = queues[self.queueID][1]
		self.queueMap = queues[self.queueID][0]
		"""
		The for loop below loops through the participants in the http request to find the id of the summoner 
		being searched for.

		Once a summoner is found, it will load up the individual stats for the summoner in the variable 
		defined as stats
		"""

		self.durationSeconds = gameInfo.duration.seconds
		self.durationMinutes = int(self.durationSeconds) // 60
		self.duration = time.strftime("%M:%S", time.gmtime(self.durationSeconds))

		self.participants = []
		player = gameInfo.participants[summoner]
		self.player = Player(self.durationMinutes, player, summoner_name)
		for player in gameInfo.participants:
			# data = player['player']
			# participant_id = player['participantId']
			# participant = match['participants'][participant_id - 1]
			summoner_name = player.summoner.name
			self.participants.append(Player(self.durationMinutes, player, summoner_name))


class Player:
	def __init__(self, durationMinutes, participant, summonerName):
		stats = participant.stats
		self.win = stats.win
		if self.win:
			self.win = 'Victory'
		else:
			self.win = 'Defeat'
		champ = Champion.objects.get(champion_id=participant.champion.id)
		self.champPhoto = champ.image
		self.champName = champ.name
		self.summonerName = summonerName
		self.spell_1 = Spell.objects.get(spellID=participant.summoner_spell_d.id)
		self.spell_2 = Spell.objects.get(spellID=participant.summoner_spell_f.id)
		self.KDA = "%s/%s/%s" % (stats.kills, stats.deaths, stats.assists)
		if stats.deaths != 0:
			self.KDA_ratio = (stats.assists + stats.kills) / stats.deaths
		self.preLevel = stats.level
		self.level = 'Level' + str(self.preLevel)
		self.baseCs = stats.total_minions_killed
		self.csPerMin = int(self.baseCs) / durationMinutes
		self.csPerMin = "%.2f" % self.csPerMin
		self.cs = str(self.baseCs) + ' (%s) cs' % self.csPerMin
		self.spell_2_image = self.spell_2.image
		self.spell_1_image = self.spell_1.image
		self.runes = list(participant.runes.keys())
		self.rune_main_1 = self.runes[0]
		self.rune_main_2 = self.runes[1]
		self.rune_main_3 = self.runes[2]
		self.rune_main_4 = self.runes[3]
		self.rune_secondary_1 = self.runes[4]
		self.rune_secondary_2 = self.runes[5]
		self.rune_main_style_id = self.runes[0].id - self.runes[0].id % 100
		self.rune_secondary_style_id = self.runes[4].id - self.runes[4].id % 100
		self.runePrefix = 'http://stelar7.no/cdragon/latest/perks'
		self.rune_main_1_icon = self.runePrefix + "/" + str(self.rune_main_1.id) + '.png'
		self.rune_main_2_icon = self.runePrefix + "/" + str(self.rune_main_2.id) + '.png'
		self.rune_main_3_icon = self.runePrefix + "/" + str(self.rune_main_3.id) + '.png'
		self.rune_main_4_icon = self.runePrefix + "/" + str(self.rune_main_4.id) + '.png'
		self.rune_secondary_1_icon = self.runePrefix + "/" + str(self.rune_secondary_1.id) + '.png'
		self.rune_secondary_2_icon = self.runePrefix + "/" + str(self.rune_secondary_2.id) + '.png'
		self.rune_main_style_icon = self.runePrefix + 'tyles/' + str(self.rune_main_style_id) + '.png'
		self.rune_secondary_style_icon = self.runePrefix + 'tyles/' + str(self.rune_secondary_style_id) + '.png'
		# self.item_1_id = stats['item1']
		# self.item_2_id = stats['item2']
		# self.item_3_id = stats['item3']
		# self.item_4_id = stats['item4']
		# self.item_5_id = stats['item5']
		self.items = participant.stats.items
		self.item_ids = []
		self.item_images = []
		for item in self.items[:6]:
			if item is None:
				self.item_ids.append(None)
				self.item_images.append("")
				continue
			self.item_ids.append(item.id)
			self.item_images.append('http://stelar7.no/cdragon/latest/items/' + str(item.id) + '.png')
		if self.items[6] is None:
			self.trinket_id = None
			self.trinket_image = ""
		else:
			self.trinket_id = self.items[6].id
			self.trinket_image = 'http://stelar7.no/cdragon/latest/items/' + str(self.trinket_id) + '.png'
		# self.item_1_image = 'http://stelar7.no/cdragon/latest/items/' + str(self.item_1_id) + '.png'
		# self.item_2_image = 'http://stelar7.no/cdragon/latest/items/' + str(self.item_2_id) + '.png'
		# self.item_3_image = 'http://stelar7.no/cdragon/latest/items/' + str(self.item_3_id) + '.png'
		# self.item_4_image = 'http://stelar7.no/cdragon/latest/items/' + str(self.item_4_id) + '.png'
		# self.item_5_image = 'http://stelar7.no/cdragon/latest/items/' + str(self.item_5_id) + '.png'

		"""for rune in runes:
			if rune['id'] == self.rune_main_1_id:
				self.rune_main_1 = rune['name']
				self.rune_main_1_description = rune['shortDesc']
				self.rune_main_style = rune['runePathName']
			elif rune['id'] == self.rune_main_2_id:
				self.rune_main_2 = rune['name']
				self.rune_main_2_description = rune['shortDesc']
			elif rune['id'] == self.rune_main_3_id:
				self.rune_main_3 = rune['name']
				self.rune_main_3_description = rune['shortDesc']
			elif rune['id'] == self.rune_main_4_id:
				self.rune_main_4 = rune['name']
				self.rune_main_4_description = rune['shortDesc']
			elif rune['id'] == self.rune_secondary_1_id:
				self.rune_secondary_1 = rune['name']
				self.rune_secondary_1_desc = rune['shortDesc']
				self.rune_secondary_style = rune['runePathName']
			elif rune['id'] == self.rune_secondary_2_id:
				self.rune_secondary_2 = rune['name']
				self.rune_secondary_2_desc = rune['shortDesc']"""


"""
				"item2": 1402,
				"item3": 3020,
				"item0": 3157,
				"item1": 3102,
				"item6": 3340,
				"item4": 3165,
				"item5": 3100,
"""


class App(TemplateView):
	template_name = 'app.html'


class Search(TemplateView):

	@staticmethod
	def display_stats(stats):
		league = stats["leagueName"]
		hot_streak = stats["hotStreak"]
		rank_tier = str(stats["tier"]).title() + ' ' + str(stats["rank"])
		lp = str(stats["leaguePoints"]) + 'lp / '
		wins_losses = str(stats["wins"]) + 'W' + ' ' + str(stats["losses"]) + 'L'
		win_ratio = 'Win Ratio ' + str(
			int(int(stats["wins"]) / (int(stats["losses"]) + int(stats["wins"])) * 100)) + "%"
		final = Stats(league, rank_tier, lp, wins_losses, win_ratio, hot_streak)
		return final

	def get(self, request, **kwargs):
		# return render(request, 'app.html', context =None)
		# def post(self, request, **kwargs):
		api_key = riot_key()
		key = RiotWatcher(api_key)
		region = 'euw1'
		profile_url_base = '//opgg-static.akamaized.net/images/profile_icons/profileIcon{0}.jpg'
		summoner_name_search = self.request.GET.get('summonerName')
		solo_tier = flex_tier = ""
		solo_stats_display = flex_stats_display = ""
		solo_win_rate = []
		flex_win_rate = []
		if Summoner.objects.filter(summoner_name=summoner_name_search).count() > 0:
			print("Found")
			summoner = Summoner.objects.get(summoner_name=summoner_name_search)
			summoner_id = summoner.summonerID
			account_id = summoner.accountID
			profile_icon_id = summoner.profileIconId
			summoner_name_search = summoner.summoner_name

			profile_url = profile_url_base.format(profile_icon_id)
			print(str(summoner_id) + ' ' + str(profile_icon_id))

		# I could of also stored this data in a table in my database but I am not due to hand restraints
		else:

			try:
				summoner = key.summoner.by_name(region, summoner_name_search)
				profile_icon_id = summoner["profileIconId"]
				profile_url = profile_url_base.format(profile_icon_id)
				summoner_id = summoner["id"]
				account_id = summoner["accountId"]
				summoner_name_search = summoner["name"]

			except HTTPError as error:
				if error.response.status_code == 429:
					# Check documentation for explanations of error codes
					summoner = (
						'''An error has occured, due to too many requests have been made to the Riot API. 
							Please try again after '''.format(error.headers['Retry']))
				elif error.response.status_code == 404:
					summoner = ('There is no summoner with that name on the region ' + region)
				return render(request, 'App.html', {
					'Summoner_Name': summoner_name_search,
				})

		# match_history = key.match.matchlist_by_account(region, account_id, end_index=5)['matches']
		match_history = cass.MatchHistory(summoner=cass.Summoner(account=account_id),end_index=5)
		games = []
		for x in match_history:
			print(x)
			games.append(Match(x, account_id, summoner_id, summoner_name_search, key))

		try:
			ranked_stats = key.league.positions_by_summoner(region, summoner_id)
			# print(ranked_stats)
			flex_stats = {}
			solo_stats = {}
			for stats in ranked_stats:
				if stats['queueType'] == "RANKED_SOLO_5x5":
					solo_stats = stats
				elif stats['queueType'] == "RANKED_FLEX_SR":
					flex_stats = stats

		except HTTPError as error:
			if error.response.status_code == 429:
				# Check documentation for explanations of error codes
				ranked_stats = (
					'''An error has occured, due to too many requests have been made to the Riot API.  Please 
					try again after '''.format(error.headers['Retry']))
			elif error.response.status_code == 404:
				ranked_stats = ('There is no summoner with that name on the region ' + region)
		if solo_stats != {}:
			solo_tier = solo_stats["tier"]
			solo_stats_display = Search.display_stats(solo_stats)
			solo_win_rate = champ_win_ratios('solo', account_id, summoner_id, summoner_name_search, key)
		if flex_stats != {}:
			flex_tier = flex_stats["tier"]
			flex_stats_display = Search.display_stats(flex_stats)
			flex_win_rate = champ_win_ratios('flex', account_id, summoner_id, summoner_name_search, key)
		highest_tier = ""
		if flex_stats == {} and solo_stats == {}:
			return render(request, 'App.html', {'has_stats': False, 'Profile_Image': profile_url,
												'Summoner_Name': summoner_name_search, })
		else:
			solo_index = tiers.index(solo_tier.lower())
			flex_index = tiers.index(flex_tier.lower())
			highest_tier = tiers[max(solo_index, flex_index)]
			return render(request, 'App.html', {'has_stats': True,
												'Summoner_Name': summoner_name_search,
												'Solo': solo_stats_display,
												'SoloChamps': solo_win_rate[:5],
												'Profile_Image': profile_url,
												'Flex': flex_stats_display,
												'FlexChamps': flex_win_rate[:5],
												'highest_tier': highest_tier,
												'Queue_Type': str(match_history),
												'matches': games,
												})


"""
class TestPageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'Test.html', context=None)
# Create your views here.
"""
