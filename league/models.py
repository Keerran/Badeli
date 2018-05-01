import cassiopeia as cass
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from .static.python.RSA import encrypt


# from .static.python.loadChampData import loadChampData


class Item(models.Model):
	ItemID = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	stacks = models.IntegerField()
	description = models.CharField(max_length=100)
	image = models.URLField()


# class Summoner(AbstractUser):
#     id = models.IntegerField(primary_key = True)
#     #username = models.CharField(max_length = 100)
#     #email = models.EmailField(max_length=254)
#     #password = models.CharField(max_length = 100)
#     profileIconId = models.IntegerField(null=True, blank=True)
#     summonerLevel = models.IntegerField(null=True, blank=True)
#     summonerID = models.IntegerField(null=True, blank=True)
#     accountID = models.IntegerField(null=True, blank=True)
#     summoner_name = models.CharField(max_length = 100)
#     def save(self,*args,**kwargs):
#         print(self.summoner_name)
#         if not self.pk and False:
#             watcher = RiotWatcher('RGAPI-29bd5816-df51-452f-929e-c920faa5bedc')
#             my_region = 'euw1'
#             Account = watcher.summoner.by_name(my_region, self.summoner_name)
#             self.accountID = Account["accountId"]
#             self.profileIconId = Account["profileIconId"]
#             self.summonerID = Account["id"]
#             self.summonerLevel = Account["summonerLevel"]
#         super().save(*args,**kwargs)
#     def set_password(self, UnsafePassword):
#         pubKey = "2257, 47"
#         encryptedPassword = (encrypt(UnsafePassword, pubKey))
#         #uses RSA encryption to encrypt the password
#         self.password = encryptedPassword
#     def check_password(self, UnsafePassword):
#         pubKey = "2257, 47"
#         encryptedPassword = (encrypt(UnsafePassword, pubKey))
#         return self.password == encryptedPassword
class Spell(models.Model):
	spellID = models.IntegerField()
	spellKey = models.CharField(max_length=100)
	spellName = models.CharField(max_length=100)
	image = models.CharField(max_length=100)
	spellDescription = models.CharField(max_length=2000)

	def __str__(self):
		return self.spellName


class Match(models.Model):
	match_id = models.IntegerField(primary_key=True)
	queue_id = models.IntegerField()
	duration = models.IntegerField()
	date = models.DateTimeField()


class PlayerCall(models.Model):
	account_id = models.IntegerField()
	date = models.DateTimeField()


class PlayerMatch(models.Model):
	TEAM = (("R", "Red"), ("B", "Blue"))
	WIN = (("W", "Victory"), ("L", "Defeat"), ("R", "Remake"))
	RANKS = (
				('U', 'Unranked'), ('B', 'Bronze'), ('S', 'Silver'),
				('G', 'Gold'), ('P', 'Platinum'), ('D', 'Diamond'),
				('M', 'Master'), ('C', 'Challenger')
			)
	WIN_DICT = {x[1]: x[0] for x in WIN}
	account_id = models.IntegerField()
	summoner_id = models.IntegerField()
	summoner_name = models.TextField(max_length="100")
	rank = models.CharField(max_length=1, choices=RANKS)
	match = models.ForeignKey(Match, on_delete=models.CASCADE)
	win = models.CharField(max_length=1, choices=WIN)
	team = models.CharField(max_length=1, choices=TEAM)
	index = models.PositiveSmallIntegerField()
	champion_id = models.IntegerField()
	spell_1 = models.ForeignKey(Spell, related_name="spell_d", on_delete=models.CASCADE)
	spell_2 = models.ForeignKey(Spell, related_name="spell_f", on_delete=models.CASCADE)
	kills = models.IntegerField()
	deaths = models.IntegerField()
	assists = models.IntegerField()
	level = models.IntegerField()
	cs = models.IntegerField()
	item1 = models.IntegerField(null=True, blank=True)
	item2 = models.IntegerField(null=True, blank=True)
	item3 = models.IntegerField(null=True, blank=True)
	item4 = models.IntegerField(null=True, blank=True)
	item5 = models.IntegerField(null=True, blank=True)
	item6 = models.IntegerField(null=True, blank=True)
	trinket = models.IntegerField(null=True, blank=True)
	rune_main_1 = models.IntegerField()
	rune_main_2 = models.IntegerField()
	rune_main_3 = models.IntegerField()
	rune_main_4 = models.IntegerField()
	rune_secondary_1 = models.IntegerField()
	rune_secondary_2 = models.IntegerField()


class Summoner(AbstractUser):
	icon_id = models.IntegerField(null=True, blank=True)
	level = models.IntegerField(null=True, blank=True)
	summoner_id = models.IntegerField(null=True, blank=True)
	account_id = models.IntegerField(null=True, blank=True)
	summoner_name = models.CharField(max_length=100)
	REQUIRED_FIELDS = ["email", "summoner_name"]

	def save(self, *args, **kwargs):
		if not self.pk:
			# api_key = riot_key()
			# watcher = RiotWatcher(api_key)
			# my_region = 'euw1'
			# account = watcher.summoner.by_name(my_region, self.summoner_name)
			account = cass.Summoner(name=self.summoner_name)
			self.account_id = account.account.id
			self.icon_id = account.profile_icon.id
			self.summoner_id = account.id
			self.level = account.level
			self.summoner_name = account.name
		super().save(*args, **kwargs)

	def set_password(self, UnsafePassword):
		pub_key = "2257, 47"
		encrypted_password = encrypt(UnsafePassword, pub_key)
		# uses RSA encryption to encrypt the password
		self.password = encrypted_password

	def check_password(self, UnsafePassword):
		pub_key = "2257, 47"
		encrypted_password = encrypt(UnsafePassword, pub_key)
		print(self.password == encrypted_password)
		return self.password == encrypted_password


# class Ranked(models.model):

class Champion(models.Model):
	champion_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	image = models.CharField(max_length=100)
	title = models.CharField(max_length=2000)
	# need to do passive
	passiveName = models.CharField(max_length=2000)
	passiveDescription = models.CharField(max_length=5000)
	passiveImage = models.CharField(max_length=2000)

	def __str__(self):
		return self.name


class ChampStat(models.Model):
	champion_id = models.ForeignKey(Champion, on_delete=models.CASCADE)
	queue_id = models.IntegerField()
	summoner_id = models.IntegerField()
	kills = models.FloatField()
	deaths = models.FloatField()
	assists = models.FloatField()
	wins = models.IntegerField()
	games = models.IntegerField()
	last_date = models.TextField(max_length=200)
	season = models.IntegerField()

	class Meta:
		unique_together = ('champion_id', 'summoner_id', 'queue_id', 'season')

	def __str__(self):
		return "%s's %s %s" % (self.summoner_id, self.queue_id, self.champion_id)


"""    
	spellKey1 = models.ForeignKey(
        Spell,on_delete=models.CASCADE,
        related_name = 'spellKey1'
        )
    spellKey2 = models.ForeignKey(
        Spell,on_delete=models.CASCADE,
        related_name = 'spellKey2'
        )
    spellKey3 = models.ForeignKey(
        Spell,on_delete=models.CASCADE,
        related_name = 'spellKey3'
        )
    spellKey4 = models.ForeignKey(
        Spell,on_delete=models.CASCADE,
        related_name = 'spellKey4'
        )
"""
