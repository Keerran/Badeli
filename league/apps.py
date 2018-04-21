from django.apps import AppConfig
from league.static.python.APIKey import riot_key
import cassiopeia as cass


class BadeliConfig(AppConfig):
	name = 'league'

	def ready(self):
		cass.set_riot_api_key(riot_key())
