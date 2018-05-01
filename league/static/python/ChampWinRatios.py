import asyncio
import concurrent

import arrow

from league.models import *
from league.models import ChampStat, Champion
from league.static.python.APIKey import cur_season


class Stats:
	def __init__(self, champion, wins, kills, deaths, assists, games):
		self.champion = champion
		c = Champion.objects.get(pk=champion)
		self.name = c.name
		self.image = c.image
		self.wins = wins
		self.kills = kills
		self.deaths = deaths
		self.assists = assists
		self.games = games


def blocking(m, summoner):
	# match = key.match.by_id("euw1", m["gameId"])

	player = m.participants[summoner]
	stats = player.stats

	win = int(stats.win)
	kills = stats.kills
	deaths = stats.deaths
	assists = stats.assists
	time = m.creation.replace(seconds=+1)
	return Stats(player.champion.id, win, kills, deaths, assists, 1), time


# champStats = {}
# if champion in champStats:
# 	s = champStats[champion]
# 	champStats[champion] = Stats(champion,s.wins+win, s.kills+kills, s.deaths+deaths, s.assists+assists, s.games+1)
# else:
# 	champStats[champion] = Stats(champion,win,kills,deaths,assists, 1)
# return champStats


async def main(loop, executor, matches, summoner):
	blocking_tasks = [
		loop.run_in_executor(executor, blocking, m, summoner)
		for m in matches
	]

	completed, pending = await asyncio.wait(blocking_tasks)
	games = []
	times = []
	for t in completed:
		x = t.result()
		games.append(x[0])
		times.append(x[1])
	time = max(times)
	return games, time


def champ_win_ratios(mode, summoner):
	season = cur_season()
	champ_stats = {}

	if mode == 'solo':
		mode = cass.Queue.ranked_solo_fives
	elif mode == 'flex':
		mode = cass.Queue.ranked_flex_fives

	c = ChampStat.objects.filter(summoner_id=summoner.id, queue_id=mode.id, season=season.id).order_by("-last_date")

	if c.exists():
		begin_time = arrow.get(c[0].last_date)
		# print(begin_time)
	else:
		begin_time = None

	# try:
	# 	champ_match_history = \
	# 		cass.MatchHistory(summoner=summoner, begin_time=begin_time, begin_index=begin_index,
	# 										queue=mode, season=season)[
	# 	#matches = list(champ_match_history)
	# except Exception:
	# 	champ_match_history = []
	# 	matches = []
	# while champ_match_history:
	# 	begin_index += 100
	# 	try:
	# 		champ_match_history = \
	# 			key.match.matchlist_by_account(summoner=summoner,begin_time=begin_time, begin_index=begin_index,
	# 											queue=mode, season=season)
	# 		matches += champ_match_history
	# 	except Exception:
	# 		break

	matches = cass.MatchHistory(summoner=summoner, begin_time=begin_time,
								queues=set([mode]), seasons=set([season]))
	executor = concurrent.futures.ThreadPoolExecutor(max_workers=123)
	loop = asyncio.new_event_loop()
	if not matches:
		games = []
	else:
		try:
			games, time = loop.run_until_complete(main(loop, executor, matches, summoner))
		finally:
			loop.close()

	for game in games:
		if game.champion in champ_stats:
			s = champ_stats[game.champion]
			champ_stats[game.champion] = Stats(game.champion, s.wins + game.wins, s.kills + game.kills,
												s.deaths + game.deaths, s.assists + game.assists, s.games + 1)
		else:
			champ_stats[game.champion] = Stats(game.champion, game.wins, game.kills, game.deaths, game.assists, 1)
	values = list(champ_stats.values())
	values = sorted(values, key=lambda x: x.games, reverse=True)
	for value in values:
		value.kills /= value.games
		value.deaths /= value.games
		value.assists /= value.games
		champ = Champion.objects.get(pk=value.champion)
		stat = ChampStat.objects.filter(champion_id=champ, summoner_id=summoner.id, queue_id=mode.id, season=season.id)
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
				champion_id=champ,
				summoner_id=summoner.id,
				queue_id=mode.id,
				kills=value.kills,
				deaths=value.deaths,
				assists=value.assists,
				wins=value.wins,
				games=value.games,
				last_date=str(time),
				season=season.id,
			).save()
	return ChampStat.objects.filter(summoner_id=summoner.id, season=season.id, queue_id=mode.id)
