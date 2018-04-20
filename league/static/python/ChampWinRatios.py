from .APIKey import *
from riotwatcher import RiotWatcher
from league.models import *
from requests import HTTPError
from league.models import ChampStat, Champion, Summoner
import asyncio,concurrent
class Stats:
	def __init__(self,champion,wins,kills,deaths,assists,games):
		self.champion = champion
		c = Champion.objects.get(pk=champion)
		self.name = c.name
		self.image = c.image
		self.wins = wins
		self.kills = kills
		self.deaths = deaths
		self.assists = assists
		self.games = games

def blocking(m, key, accountID):
	Match = key.match.by_id("euw1", m["gameId"])

	for player in Match['participantIdentities']:
		if player['player']['accountId'] == accountID or player['player']['currentAccountId'] == accountID:
			participantID = player['participantId']
			participant = Match['participants'][participantID-1]
			stats = participant['stats']
			champion = participant['championId']
			break
	win = int(stats['win'])
	kills = stats['kills']
	deaths = stats['deaths']
	assists = stats['assists']
	time = Match['gameCreation'] + 1
	return Stats(champion,win,kills,deaths,assists,1),time
	# champStats = {}
	# if champion in champStats:
	# 	s = champStats[champion]
	# 	champStats[champion] = Stats(champion,s.wins+win, s.kills+kills, s.deaths+deaths, s.assists+assists, s.games+1)
	# else:
	# 	champStats[champion] = Stats(champion,win,kills,deaths,assists, 1)
	# return champStats


async def main(loop, executor, matches, key, accountID):
	print(len(matches))
	blocking_tasks = [
		loop.run_in_executor(executor, blocking, m, key, accountID)
		for m in matches
	]

	completed, pending = await asyncio.wait(blocking_tasks)
	results = [t.result() for t in completed]
	games = [x[0] for x in results]
	time = max([x[1] for x in results])
	print(len(results))
	return games,time

def ChampWinRatios(mode, accountID, summonerID, summonerName, key):
	season = Season()
	region = 'euw1'
	champ_stats = {}
	if mode == 'solo':
		mode = 420
	elif mode == 'flex':
		mode = 440
	champions = Champion.objects.all()
	beginIndex = 0
	c = ChampStat.objects.filter(summoner_id=summonerID,queue_id=mode,season=season)
	if c.exists():
		begin_time = c[0].last_date
	else:
		begin_time = None
	try:
		ChampMatchHistory= key.match.matchlist_by_account(region, accountID, begin_time = begin_time, begin_index = beginIndex, queue = str(mode), season = str(season))['matches']
		matches = list(ChampMatchHistory)
	except Exception:
		ChampMatchHistory = []
		matches = []
	while ChampMatchHistory != []:
		beginIndex += 100
		try:
			ChampMatchHistory= key.match.matchlist_by_account(region, accountID, begin_time = begin_time, begin_index = beginIndex, queue = str(mode), season = str(season))['matches']
			matches += ChampMatchHistory
		except Exception:
			break

	print("while has ENDED")

	executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)
	loop = asyncio.new_event_loop()
	if matches == []:
		games = []
	else:
		try:
			games, time = loop.run_until_complete(main(loop,executor, matches, key, accountID))
		finally:
			loop.close()
	print("HELLO")
	for game in games:
		if game.champion in champ_stats:
			s = champ_stats[game.champion]
			champ_stats[game.champion] = Stats(game.champion,s.wins+game.wins, s.kills+game.kills, s.deaths+game.deaths, s.assists+game.assists, s.games+1)
		else:
			champ_stats[game.champion] = Stats(game.champion,game.wins,game.kills,game.deaths,game.assists, 1)
	values = list(champ_stats.values())
	values = sorted(values, key=lambda x: x.games, reverse=True)
	for value in values:
		value.kills /= value.games
		value.deaths /= value.games
		value.assists /= value.games
		champ = Champion.objects.get(pk=value.champion)
		stat = ChampStat.objects.filter(champion_id=champ,summoner_id=summonerID,queue_id=mode,season=season)
		if stat.exists():
			stat = stat[0]
			value.games += stat.games
			stat.kills = (stat.kills * stat.games + value.kills) / value.games
			stat.deaths = (stat.deaths * stat.games + value.deaths) / value.games
			stat.assists = (stat.assists * stat.games + value.assists) / value.games
			stat.wins += value.wins
			stat.games = value.games
			stat.last = time
			stat.save()
		else:
			ChampStat.objects.create(
					champion_id = champ,
					summoner_id = summonerID,
					queue_id = mode,
					kills = value.kills,
					deaths = value.deaths,
					assists = value.assists,
					wins = value.wins,
					games= value.games,
					last_date = time,
					season = season,
			).save()
	return ChampStat.objects.filter(summoner_id=summonerID, season = season, queue_id = mode)
