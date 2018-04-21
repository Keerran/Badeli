from django.apps import AppConfig
from league.static.python.APIKey import riot_key
import cassiopeia as cass


class LeagueConfig(AppConfig):
	name = 'league'

	def ready(self):
		cass.set_riot_api_key(riot_key())
		cass.set_default_region(cass.Region.europe_west)
