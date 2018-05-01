from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Summoner)
admin.site.register(Item)
admin.site.register(Champion)
admin.site.register(Spell)
admin.site.register(ChampStat)
admin.site.register(PlayerCall)
admin.site.register(Match)
admin.site.register(PlayerMatch)
