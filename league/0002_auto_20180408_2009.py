# Generated by Django 2.0.2 on 2018-04-08 16:49
from django.db import migrations
#from .models import *
from ..static.python import APIKey
from riotwatcher import RiotWatcher
from django.db import migrations
Key = APIKey.APIKey()
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
		img = 'http://stelar7.no/cdragon/latest/champion-icons/' + champ['id'] +'.png'
		passive = champ['passive']
		passiveImg = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/passive/' + passive['image']['full']
		Champion.objects.create(champion_id=int(key),name=champ['name'],image=img,title=champ['title'],
			passiveName=passive['name'],passiveDescription=passive['sanitizedDescription'],passiveImage=passiveImg).save()
def genSpells(apps, schema_editor):
	static_spell_list = watcher.static_data.summoner_spells(region, tags = 'all')
	spell_objects = []
	data = static_spell_list['data']
	Spell = apps.get_model('league','Spell')
	for key,spell in data.items():
		img = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/spell/' + spell['image']['full']
		Spell.objects.create(spellID = spell['id'], spellKey = key, spellName = spell['name'], image = img, spellDescription = spell['description']).save()
def genRunes(apps, schema_editor):
	static_rune_list = watcher.static_data.summoner_spells(region, tags = 'all')
class Migration(migrations.Migration):

	dependencies = [
		('league', '0001_initial'),
    ]

	operations = [
		migrations.RunPython(genSpells),
		migrations.RunPython(genChampions),
	]