import cassiopeia as cass
from django.apps import AppConfig

from league.static.python.APIKey import riot_key


class LeagueConfig(AppConfig):
	name = 'league'

	def ready(self):
		cass.set_riot_api_key(riot_key())
		cass.apply_settings(cass.Settings({"logging": {"print_calls": False}}))
		cass.set_default_region(cass.Region.europe_west)
