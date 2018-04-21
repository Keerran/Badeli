# Generated by Django 2.0.2 on 2018-04-08 16:49
from django.db import migrations
#from .models import *
from ..static.python import APIKey
from riotwatcher import RiotWatcher
from django.db import migrations
Key = APIKey.api_key()
watcher = RiotWatcher(Key)
region = 'na1'
def genChampions(apps, schema_editor):

	static_champ_list = watcher.static_data.champions(region, tags = 'all')
	champion_keys = static_champ_list['keys']
	data = static_champ_list['data']
	Champion = apps.get_model('league','Champion')
	champ_objects = []
	for key,name in champion_keys.items():
		champ = data[name]
		img = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/' + champ['image']['full']
		passive = champ['passive']
		passiveImg = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/passive/' + passive['image']['full']
		Champion.objects.create(champion_id=int(key),name=champ['name'],image=img,title=champ['title'],
			passiveName=passive['name'],passiveDescription=passive['sanitizedDescription'],passiveImage=passiveImg).save()
def genSpells(apps, schema_editor):
	static_spell_list = watcher.static_data.spells(region, tags = 'all')
	spell_objects = []
	Spell = apps.get_model('league','Spell')
	for key,name in static_spell_list.items():
		spell = static_spell_list['name']
		img = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/spell/' + spell['image']['full']
		Spell.objects.create(spellKey = spell['id'], spellName = spell['name'], image = img, spellDescription = spell['description']).save()
class Migration(migrations.Migration):

	dependencies = [
		('league', '0001_initial'),
    ]

	operations = [
		migrations.RunPython(genSpells),
	]