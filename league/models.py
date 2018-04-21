from django.db import models
from riotwatcher import RiotWatcher
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .static.python.RSA import generate, encrypt, decrypt
# from .static.python.loadChampData import loadChampData
from .static.python.APIKey import api_key


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
class Summoner(AbstractUser):
    profileIconId = models.IntegerField(null=True, blank=True)
    summonerLevel = models.IntegerField(null=True, blank=True)
    summonerID = models.IntegerField(null=True, blank=True)
    accountID = models.IntegerField(null=True, blank=True)
    summoner_name = models.CharField(max_length=100)
    REQUIRED_FIELDS = ["email", "summoner_name"]

    def save(self, *args, **kwargs):
        if not self.pk:
            APIKeyValue = api_key()
            watcher = RiotWatcher(APIKeyValue)
            my_region = 'euw1'
            Account = watcher.summoner.by_name(my_region, self.summoner_name)
            self.accountID = Account["accountId"]
            self.profileIconId = Account["profileIconId"]
            self.summonerID = Account["id"]
            self.summonerLevel = Account["summonerLevel"]
            self.summoner_name = Account["name"]
        super().save(*args, **kwargs)

    def set_password(self, UnsafePassword):
        pubKey = "2257, 47"
        encryptedPassword = (encrypt(UnsafePassword, pubKey))
        # uses RSA encryption to encrypt the password
        self.password = encryptedPassword

    def check_password(self, UnsafePassword):
        pubKey = "2257, 47"
        encryptedPassword = (encrypt(UnsafePassword, pubKey))
        return self.password == encryptedPassword


class Spell(models.Model):
    spellID = models.IntegerField(max_length=100)
    spellKey = models.CharField(max_length=100)
    spellName = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    spellDescription = models.CharField(max_length=2000)

    def __str__(self):
        return self.spellName


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
    last_date = models.BigIntegerField()
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
