import asyncio
import concurrent
import time
import arrow
from datapipelines import NotFoundError
from django.contrib.auth import logout, login, authenticate
from django.db.models import Max
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from requests import HTTPError
import urllib.parse as parse
from league.constants import queues
from .forms import SignUpForm
from .models import *
from .static.python.ChampWinRatios import champ_win_ratios

tiers = ["", "bronze", "silver", "gold", "platinum", "diamond", "master", "challenger"]
lanes = ["NONE", "TOP_LANE", "JUNGLE", "MID_LANE", "BOT_LANE"]


class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html', context=None)

	def post(self, request, **kwargs):
		pass


def get_index(player):
	# if player.role == "SOLO":
	if player.lane is None:
		return 0
	return lanes.index(player.lane.value)


# elif player.role is None:
# 	return 0
# else:
# 	return lanes.index(player.role.value)


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


class Player:
	def __str__(self):
		return self.summoner_name

	def __init__(self, match, participant, summonerName, finished, is_remake=None):
		self.match = match
		if finished:
			stats = participant.stats
			self.win = stats.win
			if is_remake:
				self.win = "Remake"
			elif self.win:
				self.win = 'Victory'
			else:
				self.win = 'Defeat'
		self.summoner = participant.summoner
		self.champ = Champion.objects.get(champion_id=participant.champion.id)
		self.rank = ""

		self.champPhoto = self.champ.image
		self.champName = self.champ.name
		self.summoner_name = summonerName
		self.side = participant.team.side.name
		self.spell_1 = Spell.objects.get(spellID=participant.summoner_spell_d.id)
		self.spell_2 = Spell.objects.get(spellID=participant.summoner_spell_f.id)
		if finished:
			self.kills, self.deaths, self.assists = stats.kills, stats.deaths, stats.assists
			self.KDA = "%s / %s / %s" % (stats.kills, stats.deaths, stats.assists)
			if stats.deaths != 0:
				self.KDA_ratio = (stats.assists + stats.kills) / stats.deaths
			self.preLevel = stats.level
			self.level = 'Level ' + str(self.preLevel)
			self.baseCs = stats.total_minions_killed
			self.csPerMin = int(self.baseCs) / match.duration_minutes
			self.csPerMin = "%.2f" % self.csPerMin
			self.cs = str(self.baseCs) + ' (%s) cs' % self.csPerMin
		self.spell_2_image = self.spell_2.image
		self.spell_1_image = self.spell_1.image
		if finished:
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
		if finished:
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

	def get_rank(self):
		if self.match.queue not in self.summoner.ranks:
			self.rank = "Unranked"
		else:
			rank = self.summoner.ranks[self.match.queue]
			self.rank = str(rank).strip("<>")

	def to_db(self, match, data, i):
		p = PlayerCall.objects.filter(account_id=self.summoner.account.id)
		if p.exists():
			p = p[0]
			p.date = data.timestamp.replace(seconds=+1).naive
		else:
			p = PlayerCall.objects.create(account_id=self.summoner.account.id,
										date=data.timestamp.replace(seconds=+1).naive)
		p.save()
		items = []
		for item in self.items:
			if item is None:
				items.append(None)
			else:
				items.append(item.id)
		PlayerMatch.objects.create(
			account_id=self.summoner.account.id,
			summoner_id=self.summoner.id,
			summoner_name=self.summoner.name,
			match=match,
			index=i,
			rank=self.rank[0],
			win=PlayerMatch.WIN_DICT[self.win],
			team=self.side[0].upper(),
			champion_id=self.champ.champion_id,
			spell_1_id=self.spell_1.id,
			spell_2_id=self.spell_2.id,
			kills=self.kills,
			deaths=self.deaths,
			assists=self.assists,
			level=self.preLevel,
			cs=self.baseCs,
			item1=items[0],
			item2=items[1],
			item3=items[2],
			item4=items[3],
			item5=items[4],
			item6=items[5],
			trinket=items[6],
			rune_main_1=self.rune_main_1.id,
			rune_main_2=self.rune_main_2.id,
			rune_main_3=self.rune_main_3.id,
			rune_main_4=self.rune_main_4.id,
			rune_secondary_1=self.rune_secondary_1.id,
			rune_secondary_2=self.rune_secondary_2.id
		).save()


class PlayerDB:
	def __init__(self, player, match, summoner_name):
		self.win = player.get_win_display()
		self.match = match
		self.champ = Champion.objects.get(champion_id=player.champion_id)
		# summoner = cass.Summoner(id=player.summoner_id)
		# rank = summoner.ranks.get(match.queue, None)
		self.side = player.team
		self.champPhoto = self.champ.image
		self.champName = self.champ.name
		self.summoner_name = summoner_name
		self.spell_1 = player.spell_1
		self.spell_2 = player.spell_2
		self.rank = player.get_rank_display
		self.kills, self.deaths, self.assists = player.kills, player.deaths, player.assists
		self.KDA = "%s / %s / %s" % (player.kills, player.deaths, player.assists)
		if player.deaths != 0:
			self.KDA_ratio = (player.assists + player.kills) / player.deaths
		self.preLevel = player.level
		self.level = 'Level ' + str(self.preLevel)
		self.baseCs = player.cs
		self.csPerMin = int(self.baseCs) / match.duration_minutes
		self.csPerMin = "%.2f" % self.csPerMin
		self.cs = str(self.baseCs) + ' (%s) cs' % self.csPerMin
		self.spell_2_image = self.spell_2.image
		self.spell_1_image = self.spell_1.image
		self.rune_main_1 = player.rune_main_1
		self.rune_main_2 = player.rune_main_2
		self.rune_main_3 = player.rune_main_3
		self.rune_main_4 = player.rune_main_4
		self.rune_secondary_1 = player.rune_secondary_1
		self.rune_secondary_2 = player.rune_secondary_2
		self.rune_main_style_id = self.rune_main_1 - self.rune_main_1 % 100
		self.rune_secondary_style_id = self.rune_secondary_1 - self.rune_secondary_1 % 100
		self.runePrefix = 'http://stelar7.no/cdragon/latest/perks'
		self.rune_main_1_icon = self.runePrefix + "/" + str(self.rune_main_1) + '.png'
		self.rune_main_2_icon = self.runePrefix + "/" + str(self.rune_main_2) + '.png'
		self.rune_main_3_icon = self.runePrefix + "/" + str(self.rune_main_3) + '.png'
		self.rune_main_4_icon = self.runePrefix + "/" + str(self.rune_main_4) + '.png'
		self.rune_secondary_1_icon = self.runePrefix + "/" + str(self.rune_secondary_1) + '.png'
		self.rune_secondary_2_icon = self.runePrefix + "/" + str(self.rune_secondary_2) + '.png'
		self.rune_main_style_icon = self.runePrefix + 'tyles/' + str(self.rune_main_style_id) + '.png'
		self.rune_secondary_style_icon = self.runePrefix + 'tyles/' + str(self.rune_secondary_style_id) + '.png'
		# self.item_1_id = stats['item1']
		# self.item_2_id = stats['item2']
		# self.item_3_id = stats['item3']
		# self.item_4_id = stats['item4']
		# self.item_5_id = stats['item5']
		self.item_ids = []
		self.item_images = []
		for i in range(6):
			item = getattr(player, "item{0}".format(i + 1))
			if item is None:
				self.item_ids.append(None)
				self.item_images.append("")
				continue
			self.item_ids.append(item)
			self.item_images.append('http://stelar7.no/cdragon/latest/items/' + str(item) + '.png')
		if player.trinket is None:
			self.trinket_id = None
			self.trinket_image = ""
		else:
			self.trinket_id = player.trinket
			self.trinket_image = 'http://stelar7.no/cdragon/latest/items/' + str(self.trinket_id) + '.png'


class MatchData:
	def __init__(self, game_info, accountID, summonerID, summoner_name, finished=True):  # , key):
		self.account_id = accountID
		summoner = cass.Summoner(account=accountID)
		self.summoner_id = summonerID
		self.summonerName = summoner_name
		self.game = game_info
		self.player_stats = game_info.participants[summoner]
		self.timestamp = self.game.creation
		self.game_id = self.game.id
		# self.role = self.game.role
		# self.lane = self.game.lane
		self.champion_id = self.player_stats.champion.id
		# match = key.match.by_id(region, self.gameID)
		self.queue = game_info.queue
		self.queue_id = game_info.queue.id
		self.queue_type = queues[self.queue_id][1]
		self.queue_map = queues[self.queue_id][0]
		"""
		The for loop below loops through the participants in the http request to find the id of the summoner 
		being searched for.

		Once a summoner is found, it will load up the individual stats for the summoner in the variable 
		defined as stats
		"""
		self.duration_seconds = game_info.duration.seconds
		self.duration_minutes = int(self.duration_seconds) // 60
		self.duration = time.strftime("%M:%S", time.gmtime(self.duration_seconds))

		self.participants = []
		player = game_info.participants[summoner]
		is_remake = game_info.is_remake if finished else None
		self.player = Player(self, player, summoner_name, finished, is_remake)

		self.blue_team = []
		self.red_team = []
		# if finished:
		# 	blue_team = sorted(game_info.blue_team.participants, key=get_index)
		# 	red_team = sorted(game_info.red_team.participants, key=get_index)
		# else:
		blue_team = game_info.blue_team.participants
		red_team = game_info.red_team.participants
		for player in blue_team:
			# data = player['player']
			# participant_id = player['participantId']
			# participant = match['participants'][participant_id - 1]
			summoner_name = player.summoner.name
			if player.summoner == summoner:
				summoner_name = "<b>{0}</b>".format(summoner_name)
			self.blue_team.append(
				Player(self, player, summoner_name, finished, is_remake))

		for player in red_team:
			# data = player['player']
			# participant_id = player['participantId']
			# participant = match['participants'][participant_id - 1]
			summoner_name = player.summoner.name
			if player.summoner == summoner:
				summoner_name = "<b>{0}</b>".format(summoner_name)
			self.red_team.append(Player(self, player, summoner_name, finished, is_remake))

	def get_ranks(self):
		for player in self.blue_team + self.red_team:
			player.get_rank()

	def to_db(self):
		m = Match.objects.create(
			match_id=self.game_id,
			queue_id=self.queue.id,
			duration=self.duration_seconds,
			date=self.timestamp.naive
		)
		m.save()
		for i, player in enumerate(self.blue_team):
			player.to_db(m, self, i)
		for i, player in enumerate(self.red_team):
			player.to_db(m, self, i)


class MatchDB:
	def __init__(self, model, summoner):
		players = PlayerMatch.objects.filter(match_id=model.id).select_related()
		model = players[0].match
		player_stats = players.get(account_id=summoner.account.id)
		self.account_id = summoner.account.id
		self.summoner = summoner.id
		self.summonerName = summoner.name
		# self.timestamp = model.date
		self.game_id = model.match_id
		# self.role = self.game.role
		# self.lane = self.game.lane
		self.champion_id = player_stats.champion_id
		# match = key.match.by_id(region, self.gameID)
		self.queue_id = model.queue_id
		self.queue = cass.Queue.from_id(self.queue_id)
		self.queue_type = queues[self.queue_id][1]
		self.queue_map = queues[self.queue_id][0]
		"""
		The for loop below loops through the participants in the http request to find the id of the summoner 
		being searched for.

		Once a summoner is found, it will load up the individual stats for the summoner in the variable 
		defined as stats
		"""
		self.duration_seconds = model.duration
		self.duration_minutes = int(self.duration_seconds) // 60
		self.duration = time.strftime("%M:%S", time.gmtime(self.duration_seconds))

		self.participants = []
		# player = gameInfo.participants[summoner]
		self.player = PlayerDB(players.get(summoner_id=summoner.id), self, summoner.name)

		self.blue_team = []
		self.red_team = []

		# if finished:
		# 	blue_team = sorted(gameInfo.blue_team.participants, key=get_index)
		# 	red_team = sorted(gameInfo.red_team.participants, key=get_index)
		# else:
		# 	blue_team = gameInfo.blue_team.participants
		# 	red_team = gameInfo.red_team.participants
		blue_team = players.filter(team="B").order_by("index")
		red_team = players.filter(team="R").order_by("index")
		for player in blue_team:
			# data = player['player']
			# participant_id = player['participantId']
			# participant = match['participants'][participant_id - 1]
			# s = cass.Summoner(id=player.summoner_id)
			summoner_name = player.summoner_name
			if player.account_id == summoner.account.id:
				summoner_name = "<b>{0}</b>".format(summoner.name)
			self.blue_team.append(PlayerDB(player, self, summoner_name))

		for player in red_team:
			# data = player['player']
			# participant_id = player['participantId']
			# participant = match['participants'][participant_id - 1]
			summoner_name = player.summoner_name
			if player.account_id == summoner.account.id:
				summoner_name = "<b>{0}</b>".format(summoner_name)
			self.red_team.append(PlayerDB(player, self, summoner_name))


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


def blocking(x, summoner, summoner_name_search):
	db = Match.objects.filter(match_id=x.id)
	if db.exists():
		m = MatchDB(x, summoner)
	else:
		m = MatchData(x, summoner.account.id, summoner.id, summoner_name_search)  # , key))
	return m


async def main(loop, executor, matches, summoner, summoner_name_search):
	blocking_tasks = [
		loop.run_in_executor(executor, blocking, x, summoner, summoner_name_search)
		for x in matches
	]

	completed, pending = await asyncio.wait(blocking_tasks)
	results = []
	for t in completed:
		results.append(t.result())

	return results


class Search(TemplateView):

	@staticmethod
	def display_stats(stats):
		league = stats.name
		hot_streak = stats.hot_streak
		rank_tier = str(stats.tier.name).title() + ' ' + str(stats.division.value)
		lp = str(stats.league_points) + 'lp'
		wins_losses = str(stats.wins) + 'W' + ' ' + str(stats.losses) + 'L'
		win_ratio = 'Win Ratio ' + str(
			int(int(stats.wins) / (int(stats.losses) + int(stats.wins)) * 100)) + "%"
		final = Stats(league, rank_tier, lp, wins_losses, win_ratio, hot_streak)
		return final

	def get(self, request, **kwargs):
		# return render(request, 'app.html', context =None)
		# def post(self, request, **kwargs):
		profile_url_base = '//opgg-static.akamaized.net/images/profile_icons/profileIcon{0}.jpg'
		summoner_name_search = self.request.GET.get('summonerName')
		summoner_name_search = parse.quote(summoner_name_search)
		solo_tier = flex_tier = ""
		solo_stats_display = flex_stats_display = ""
		solo_win_rate = []
		flex_win_rate = []

		try:
			summoner = cass.Summoner(name=summoner_name_search)
			if not summoner.exists:
				return redirect("home")
			account_id = summoner.account.id
			icon_id = summoner.profile_icon.id
			profile_url = profile_url_base.format(icon_id)
			summoner_id = summoner.id
			summoner_name_search = summoner.name

		except HTTPError as error:
			if error.response.status_code == 429:
				# Check documentation for explanations of error codes
				summoner = (
					'''An error has occured, due to too many requests have been made to the Riot API. 
						Please try again after '''.format(error.headers['Retry']))
			elif error.response.status_code == 404:
				summoner = ('There is no summoner with that name on the region ' + "EUW1")
			return render(request, 'App.html', {
				'Summoner_Name': summoner_name_search,
			})

		# match_history = key.match.matchlist_by_account(region, account_id, end_index=5)['matches']
		# ms = PlayerCall.objects.filter(account_id=summoner.account.id)
		# creation = ms.aggregate(Max('date'))['date__max']
		ms = PlayerMatch.objects.filter(account_id=summoner.account.id).order_by("-match__date")
		# print(creation)
		# if creation is not None:
		# 	creation = arrow.get(creation)
		match_history = cass.MatchHistory(summoner=summoner, end_index=10)
		print("CREATION {0}".format(len(match_history)))
		ms = ms[:10 - len(match_history)]
		games = []

		loop = asyncio.new_event_loop()
		executor = concurrent.futures.ThreadPoolExecutor(max_workers=123)

		try:
			games = loop.run_until_complete(main(loop, executor, match_history, summoner, summoner_name_search))
		finally:
			loop.close()
		for x in games:
			if isinstance(x, MatchData):
				x.get_ranks()
				x.to_db()
		try:
			current_match = MatchData(summoner.current_match, account_id, summoner_id, summoner_name_search, False)
		except NotFoundError:
			current_match = None

		try:
			# key = RiotWatcher(riot_key())
			# ranked_stats = key.league.positions_by_summoner("EUW1", summoner_id)
			# print(ranked_stats)
			flex_stats = None
			solo_stats = None
			for stats in summoner.league_positions:
				if stats.queue == cass.Queue.ranked_solo_fives:
					solo_stats = stats
				elif stats.queue == cass.Queue.ranked_flex_fives:
					flex_stats = stats

		except HTTPError as error:
			if error.response.status_code == 429:
				# Check documentation for explanations of error codes
				ranked_stats = (
					'''An error has occured, due to too many requests have been made to the Riot API.  Please 
					try again after '''.format(error.headers['Retry']))
			elif error.response.status_code == 404:
				ranked_stats = ('There is no summoner with that name on the region ' + "EUW1")
		if solo_stats is not None:
			solo_tier = solo_stats.tier.name
			solo_stats_display = Search.display_stats(solo_stats)
			solo_win_rate = champ_win_ratios('solo', summoner)
		if flex_stats is not None:
			flex_tier = flex_stats.tier.name
			flex_stats_display = Search.display_stats(flex_stats)
			flex_win_rate = champ_win_ratios('flex', summoner)
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
			                                    'current_match': current_match,
			                                    })


"""
class TestPageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'Test.html', context=None)
# Create your views here.
"""
