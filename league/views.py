from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import TemplateView
from django.conf.urls import url
from django.contrib.auth import login, authenticate, logout 
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .static.python.RSA import generate, encrypt, decrypt
from .models import *
from requests import HTTPError
from .static.python.APIKey import APIKey, Season
import datetime
import time
import json
from.static.python.ChampWinRatios import ChampWinRatios
tiers = ["","bronze","silver","gold","platinum","diamond","master","challenger"]
#queues ={0: ["Custom", ""], 2: ["Summoner’s Rift", "5v5 Blind Pick"], 73: ["Howling Abyss", "2v2 Snowdown Showdown"], 75: ["Summoner’s Rift", "6v6 Hexakill"], 76: ["Summoner’s Rift", "Ultra Rapid Fire"], 78: ["Howling Abyss", "One For All: Mirror Mode"], 83: ["Summoner’s Rift", "Co-op vs AI Ultra Rapid Fire"], 91: ["Summoner’s Rift", "Doom Bots Rank 1"], 100: ["Butcher's Bridge", "5v5 ARAM"], 300: ["Howling Abyss", "Legend of the Poro King"], 313: ["Summoner’s Rift", "Black Market Brawlers"], 315: ["Summoner’s Rift", "Nexus Siege"], 318: ["Summoner’s Rift", "ARURF"], 400: ["Summoner’s Rift", "5v5 Draft Pick"], 410: ["Summoner’s Rift", "5v5 Ranked Dynamic"], 420: ["Summoner’s Rift", "Ranked Solo"], 430: ["Summoner’s Rift", "5v5 Blind Pick"], 440: ["Summoner’s Rift", "5v5 Ranked Flex"], 450: ["Howling Abyss", "5v5 ARAM"], 460: ["Twisted Treeline", "3v3 Blind Pick"], 470: ["Twisted Treeline", "3v3 Ranked Flex"], 600: ["Summoner’s Rift", "Blood Hunt Assassin"], 610: ["Cosmic Ruins", "Dark Star: Singularity"], 800: ["Twisted Treeline", "Co-op vs. AI Intermediate Bot"], 810: ["Twisted Treeline", "Co-op vs. AI Intro Bot"], 820: ["Twisted Treeline", "Co-op vs. AI Beginner Bot"], 830: ["Summoner’s Rift", "Co-op vs. AI Intro Bot"], 840: ["Summoner’s Rift", "Co-op vs. AI Beginner Bot"], 850: ["Summoner’s Rift", "Co-op vs. AI Intermediate Bot"], 900: ["Summoner’s Rift", "ARURF"], 910: ["Crystal Scar", "Ascension"], 920: ["Howling Abyss", "Legend of the Poro King"], 940: ["Summoner’s Rift", "Nexus Siege"], 950: ["Summoner’s Rift", "Doom Bots Voting"], 960: ["Summoner’s Rift", "Doom Bots Standard"], 980: ["Valoran City Park", "Star Guardian Invasion: Normal"], 990: ["Valoran City Park", "Star Guardian Invasion: Onslaught"], 1000: ["Overcharge", "PROJECT: Hunters"], 1010: ["Summoner’s Rift", "Snow ARURF"], 1020: ["Summoner’s Rift", "One for All"]}
queues = {0: ['Custom',''], 2: ["Summoner's Rift", '5v5 Blind Pick'], 4: ["Summoner's Rift", '5v5 Ranked Solo'], 6: ["Summoner's Rift", '5v5 Ranked Premade'], 7: ["Summoner's Rift", 'Co-op vs AI'], 8: ['Twisted Treeline', '3v3 Normal'], 9: ['Twisted Treeline', '3v3 Ranked Flex'], 14: ["Summoner's Rift", '5v5 Draft Pick'], 16: ['Crystal Scar', '5v5 Dominion Blind Pick'], 17: ['Crystal Scar', '5v5 Dominion Draft Pick'], 25: ['Crystal Scar', 'Dominion Co-op vs AI'], 31: ["Summoner's Rift", 'Co-op vs AI Intro Bot'], 32: ["Summoner's Rift", 'Co-op vs AI Beginner Bot'], 33: ["Summoner's Rift", 'Co-op vs AI Intermediate Bot'], 41: ['Twisted Treeline', '3v3 Ranked Team'], 42: ["Summoner's Rift", '5v5 Ranked Team'], 52: ['Twisted Treeline', 'Co-op vs AI'], 61: ["Summoner's Rift", '5v5 Team Builder'], 65: ['Howling Abyss', '5v5 ARAM'], 70: ["Summoner's Rift", 'One for All'], 72: ['Howling Abyss', '1v1 Snowdown Showdown'], 73: ['Howling Abyss', '2v2 Snowdown Showdown'], 75: ["Summoner's Rift", '6v6 Hexakill'], 76: ["Summoner's Rift", 'Ultra Rapid Fire'], 78: ['Howling Abyss', 'One For All: Mirror Mode'], 83: ["Summoner's Rift", 'Co-op vs AI Ultra Rapid Fire'], 91: ["Summoner's Rift", 'Doom Bots Rank 1'], 92: ["Summoner's Rift", 'Doom Bots Rank 2'], 93: ["Summoner's Rift", 'Doom Bots Rank 5'], 96: ['Crystal Scar', 'Ascension'], 98: ['Twisted Treeline', '6v6 Hexakill'], 100: ["Butcher's Bridge", '5v5 ARAM'], 300: ['Howling Abyss', 'Legend of the Poro King'], 310: ["Summoner's Rift", 'Nemesis'], 313: ["Summoner's Rift", 'Black Market Brawlers'], 315: ["Summoner's Rift", 'Nexus Siege'], 317: ['Crystal Scar', 'Definitely Not Dominion'], 318: ["Summoner's Rift", 'ARURF'], 325: ["Summoner's Rift", 'All Random'], 400: ["Summoner's Rift", '5v5 Draft Pick'], 410: ["Summoner's Rift", '5v5 Ranked Dynamic'], 420: ["Summoner's Rift", '5v5 Ranked Solo'], 430: ["Summoner's Rift", '5v5 Blind Pick'], 440: ["Summoner's Rift", '5v5 Ranked Flex'], 450: ['Howling Abyss', '5v5 ARAM'], 460: ['Twisted Treeline', '3v3 Blind Pick'], 470: ['Twisted Treeline', '3v3 Ranked Flex'], 600: ["Summoner's Rift", 'Blood Hunt Assassin'], 610: ['Cosmic Ruins', 'Dark Star: Singularity'], 800: ['Twisted Treeline', 'Co-op vs. AI Intermediate Bot'], 810: ['Twisted Treeline', 'Co-op vs. AI Intro Bot'], 820: ['Twisted Treeline', 'Co-op vs. AI Beginner Bot'], 830: ["Summoner's Rift", 'Co-op vs. AI Intro Bot'], 840: ["Summoner's Rift", 'Co-op vs. AI Beginner Bot'], 850: ["Summoner's Rift", 'Co-op vs. AI Intermediate Bot'], 900: ["Summoner's Rift", 'ARURF'], 910: ['Crystal Scar', 'Ascension'], 920: ['Howling Abyss', 'Legend of the Poro King'], 940: ["Summoner's Rift", 'Nexus Siege'], 950: ["Summoner's Rift", 'Doom Bots Voting'], 960: ["Summoner's Rift", 'Doom Bots Standard'], 980: ['Valoran City Park', 'Star Guardian Invasion: Normal'], 990: ['Valoran City Park', 'Star Guardian Invasion: Onslaught'], 1000: ['Overcharge', 'PROJECT: Hunters'], 1010: ["Summoner's Rift", 'Snow ARURF games'], 1020: ["Summoner's Rift", "One for All"]}
# Create your views here.
runes = [{"id":8134,"key":"IngeniousHunter","name":"Ingenious Hunter","shortDesc":"<b>Unique</b> <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Takedown'>takedowns</lol-uikit-tooltipped-keyword> grant permanent Active Item <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_CDR'>CDR</lol-uikit-tooltipped-keyword> (includes Trinkets).","longDesc":"Gain @StartingActiveItemCDR.0*100@% <b>Active Item CDR</b> plus an additional @ActiveItemCDRPerStack.0*100@% per <i>Bounty Hunter</i> stack (includes Trinkets).<br><br>Earn a <i>Bounty Hunter</i> stack the first time you get a takedown on each enemy champion.","icon":"ASSETS/Perks/Styles/Domination/IngeniousHunter/IngeniousHunter.dds","runePathId":8100,"runePathName":"Domination"},{"id":8299,"key":"LastStand","name":"Last Stand","shortDesc":"Deal more damage to champions while you are low on health.","longDesc":"Deal @MinBonusDamagePercent.0*100@% - @MaxBonusDamagePercent.0*100@% increased damage to champions while you are below @HealthThresholdStart.0*100@% health. Max damage gained at @HealthThresholdEnd.0*100@% health.","icon":"ASSETS/Perks/Styles/Sorcery/LastStand/LastStand.dds","runePathId":8000,"runePathName":"Precision"},{"id":8453,"key":"Revitalize","name":"Revitalize","shortDesc":"Heals and shields you cast or receive are @StandardAmp.0@% stronger and increased by an additional @ExtraAmp.0@% on low health targets.","longDesc":"Heals and shields you cast or receive are @StandardAmp.0@% stronger and increased by an additional @ExtraAmp.0@% on targets below @HealthCutoff.0@% health.","icon":"ASSETS/Perks/Styles/Resolve/Revitalize/Revitalize.dds","runePathId":8400,"runePathName":"Resolve"},{"id":8135,"key":"RavenousHunter","name":"Ravenous Hunter","shortDesc":"<b>Unique</b> <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Takedown'>takedowns</lol-uikit-tooltipped-keyword> grant permanent healing from ability damage. ","longDesc":"Heal for a percentage of the damage dealt by your abilities.<br>Healing: @StartingOmnivamp*100@% + @OmnivampPerStack*100@% per <i>Bounty Hunter</i> stack. <br><br>Earn a <i>Bounty Hunter</i> stack the first time you get a takedown on each enemy champion.<br><rules><br>Healing reduced to one third for Area of Effect abilities.</rules><br>","icon":"ASSETS/Perks/Styles/Domination/RavenousHunter/RavenousHunter.dds","runePathId":8100,"runePathName":"Domination"},{"id":8410,"key":"ApproachVelocity","name":"Approach Velocity","shortDesc":"Bonus <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_MS'>MS</lol-uikit-tooltipped-keyword> towards nearby ally champions that are <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_ImpairMov'>movement impaired</lol-uikit-tooltipped-keyword> or enemy champions that you impair.","longDesc":"Gain @MovementSpeedPercentBonus.0*100@% Movement Speed towards nearby ally champions that are movement impaired or enemy champions that you impair. <br><br>Range: @ActivationDistance@","icon":"ASSETS/Perks/Styles/Resolve/ApproachVelocity/ApproachVelocity.dds","runePathId":8300,"runePathName":"Inspiration"},{"id":9103,"key":"LegendBloodline","name":"Legend: Bloodline","shortDesc":"<lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Takedown'>Takedowns</lol-uikit-tooltipped-keyword> on enemies grant permanent<b> Lifesteal</b>. ","longDesc":"Gain @LifeStealPerStack*100@% life steal for every <i>Legend</i> stack (max @MaxLegendStacks@ stacks).<br><br>Earn progress toward <i>Legend</i> stacks for every champion takedown, epic monster takedown, large monster kill, and minion kill.","icon":"ASSETS/Perks/Styles/Precision/Legend_Infamy.dds","runePathId":8000,"runePathName":"Precision"},{"id":8014,"key":"CoupDeGrace","name":"Coup de Grace","shortDesc":"Deal more damage to low health enemy champions.","longDesc":"Deal @BonusPercentDamage.0 *100@% more damage to champions who have less than @EnemyHealthPercentageThreshold*100@% health.<br><br>Additionally, takedowns on champions grant an <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'><font color='#48C4B7'>adaptive</font></lol-uikit-tooltipped-keyword> bonus of @AdaptiveForce.-1*0.6@ Attack Damage or @AdaptiveForce@ Ability Power for @Duration@s.","icon":"ASSETS/Perks/Styles/Precision/CoupDeGrace/CoupDeGrace.dds","runePathId":8000,"runePathName":"Precision"},{"id":8451,"key":"Overgrowth","name":"Overgrowth","shortDesc":"Gain additional permanent max health when minions or monsters die near you.","longDesc":"Permanently gain @MaxHealthRatioPerTier*100@% maximum health for every @UnitsPerTier@ monsters or enemy minions that die near you.","icon":"ASSETS/Perks/Styles/Resolve/Overgrowth/Overgrowth.dds","runePathId":8400,"runePathName":"Resolve"},{"id":9101,"key":"Overheal","name":"Overheal","shortDesc":"Excess healing on you becomes a shield.","longDesc":"Excess healing on you becomes a shield, for up to @ShieldCapRatio.0*100@% of your total health + @MaxBaseShieldCap@.<br><br>Shield is built up from @ShieldGenerationRateSelf.0*100@% of excess self-healing, or @ShieldGenerationRateOtherMax.0*100@% of excess healing from allies.","icon":"ASSETS/Perks/Styles/Precision/Overheal.dds","runePathId":8000,"runePathName":"Precision"},{"id":8210,"key":"Transcendence","name":"Transcendence","shortDesc":"Gain @MaxCDR*100@% <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_CDR'>CDR</lol-uikit-tooltipped-keyword> when you reach level @LevelToTurnOn@. Excess CDR becomes AP or AD, <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'>adaptive</lol-uikit-tooltipped-keyword>.","longDesc":"Gain @MaxCDR*100@% CDR when you reach level @LevelToTurnOn@.<br><br>Each percent of CDR exceeding the CDR limit is converted to an <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'><font color='#48C4B7'>adaptive</font></lol-uikit-tooltipped-keyword> bonus of @AdaptiveForce.-1*0.6@ Attack Damage or @AdaptiveForce@ Ability Power.","icon":"ASSETS/Perks/Styles/Sorcery/Transcendence/Transcendence.dds","runePathId":8200,"runePathName":"Sorcery"},{"id":8138,"key":"EyeballCollection","name":"Eyeball Collection","shortDesc":"Collect eyeballs for champion and ward <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Takedown'>takedowns</lol-uikit-tooltipped-keyword>. Gain permanent AD or AP, <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'>adaptive</lol-uikit-tooltipped-keyword> for each eyeball plus bonus upon collection completion.","longDesc":"Collect eyeballs for champion and ward takedowns. Gain an <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'><font color='#48C4B7'>adaptive</font></lol-uikit-tooltipped-keyword> bonus of @AdaptiveForce.-1*0.6@ Attack Damage or @AdaptiveForce@ Ability Power, per eyeball collected. <br><br>Upon completing your collection at @MaxEyeballs@ eyeballs, additionally gain an <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'><font color='#48C4B7'>adaptive</font></lol-uikit-tooltipped-keyword> bonus of @CompletionBonus.-1*0.6@ Attack Damage, or @CompletionBonus@ Ability Power.<br><br>Collect @StacksPerTakedown@ eyeballs per champion kill, @StacksPerAssist@ per assist, and @StacksPerWard@ per ward takedown.","icon":"ASSETS/Perks/Styles/Domination/EyeballCollection/EyeballCollection.dds","runePathId":8100,"runePathName":"Domination"},{"id":8017,"key":"CutDown","name":"Cut Down","shortDesc":"Deal more damage to champions with more max health than you.","longDesc":"Deal @MinBonusDamagePercent.0*100@% more damage to champions with @MinHealthDifference@ more max health than you, increasing to @MaxBonusDamagePercent.0*100@% at @MaxHealthDifference@ more max health.","icon":"ASSETS/Perks/Styles/Precision/CutDown/CutDown.dds","runePathId":8000,"runePathName":"Precision"},{"id":8139,"key":"TasteOfBlood","name":"Taste of Blood","shortDesc":"Heal when you damage an enemy champion.","longDesc":"Heal when you damage an enemy champion.<br><br>Healing: @HealAmount@-@HealAmountMax@ (+@ADRatio.-1@ bonus AD, +@APRatio.-1@ AP) health (based on level)<br><br>Cooldown: @Cooldown@s","icon":"ASSETS/Perks/Styles/Domination/TasteOfBlood/GreenTerror_TasteOfBlood.dds","runePathId":8100,"runePathName":"Domination"},{"id":8136,"key":"ZombieWard","name":"Zombie Ward","shortDesc":"After killing a ward, a friendly Zombie Ward is raised in its place. When your wards expire, they also reanimate as Zombie Wards.","longDesc":"After killing a ward, a friendly Zombie Ward is raised in its place. Additionally, when your wards expire, they reanimate as Zombie Wards.<br><br>Zombie Wards are visible, last for @WardDurationTooltipMin@ - @WardDuration@s and don't count towards your ward limit.","icon":"ASSETS/Perks/Styles/Domination/ZombieWard/ZombieWard.dds","runePathId":8100,"runePathName":"Domination"},{"id":9104,"key":"LegendAlacrity","name":"Legend: Alacrity","shortDesc":"<lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Takedown'>Takedowns</lol-uikit-tooltipped-keyword> on enemies grant permanent <b>Attack Speed</b>. ","longDesc":"Gain @AttackSpeedBase*100@% attack speed plus an additional @AttackSpeedPerStack*100@% for every <i>Legend</i> stack (max @MaxLegendStacks@ stacks).<br><br>Earn progress toward <i>Legend</i> stacks for every champion takedown, epic monster takedown, large monster kill, and minion kill.","icon":"ASSETS/Perks/Styles/Precision/Legend_Heroism.dds","runePathId":8000,"runePathName":"Precision"},{"id":9105,"key":"LegendTenacity","name":"Legend: Tenacity","shortDesc":"<lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Takedown'>Takedowns</lol-uikit-tooltipped-keyword> on enemies grant permanent <b>Tenacity</b>. ","longDesc":"Gain @TenacityBase*100@% tenacity plus an additional @TenacityPerStack*100@% for every <i>Legend</i> stack (max @MaxLegendStacks@ stacks).<br><br>Earn progress toward <i>Legend</i> stacks for every champion takedown, epic monster takedown, large monster kill, and minion kill.","icon":"ASSETS/Perks/Styles/Precision/Legend_Tenacity.dds","runePathId":8000,"runePathName":"Precision"},{"id":8214,"key":"SummonAery","name":"Summon Aery","shortDesc":"Your attacks and abilities send Aery to a target, damaging enemies or shielding allies.","longDesc":"Your attacks and abilities send Aery to a target, damaging enemy champions or shielding allies.<br><br>Damage: @DamageBase@ - @DamageMax@ based on level (+<scaleAP>@DamageAPRatio.-1@ AP</scaleAP> and +<scaleAD>@DamageADRatio.-1@ bonus AD</scaleAD>)<br>Shield: @ShieldBase@ - @ShieldMax@ based on level (+<scaleAP>@ShieldRatio.-1@ AP</scaleAP> and +<scaleAD>@ShieldRatioAD.-1@ bonus AD</scaleAD>) <br><br>Aery cannot be sent out again until she returns to you.","icon":"ASSETS/Perks/Styles/Sorcery/SummonAery/SummonAery.dds","runePathId":8200,"runePathName":"Sorcery"},{"id":8010,"key":"Conqueror","name":"Conqueror","shortDesc":"After @ThresholdTime@ seconds in combat, your first attack against an enemy champion grants you AD and converts some of your damage to true damage.","longDesc":"After @ThresholdTime@ seconds in combat, your first attack against an enemy champion grants you @BaseAD@ - @MaxAD@ AD, based on level, for @BuffDuration@ seconds and converts @TrueDamageBase*100@% of your damage to champions to true damage.<br><br><rules>Melee Only: Damaging enemy champions refreshes this buff.</rules>","icon":"ASSETS/Perks/Styles/Precision/Conqueror/Conqueror.dds","runePathId":8000,"runePathName":"Precision"},{"id":8008,"key":"LethalTempo","name":"Lethal Tempo","shortDesc":"@LeadInDelay.1@s after damaging a champion gain a large amount of Attack Speed. Lethal Tempo allows you to temporarily exceed the attack speed limit.","longDesc":"@LeadInDelay.1@s after damaging a champion gain @AttackSpeedMin*100@ - @AttackSpeedMax*100@% Attack Speed (based on level) for @AttackSpeedBuffDurationMin@s. Attacking a champion extends the effect to @AttackSpeedBuffDurationMax@s.<br><br>Cooldown: @Cooldown@s<br><br>Lethal Tempo allows you to temporarily exceed the attack speed limit.","icon":"ASSETS/Perks/Styles/Precision/FlowofBattle/FlowofBattleTemp.dds","runePathId":8000,"runePathName":"Precision"},{"id":8009,"key":"PresenceOfMind","name":"Presence of Mind","shortDesc":"Takedowns restore @PercentManaRestore*100@% of your maximum mana and refund @UltimateCooldownRefund*100@% of your ultimate's cooldown.","longDesc":"Takedowns restore @PercentManaRestore*100@% of your maximum mana and refund @UltimateCooldownRefund*100@% of your ultimate's cooldown.","icon":"ASSETS/Perks/Styles/Precision/LastResort/LastResortIcon.dds","runePathId":8000,"runePathName":"Precision"},{"id":8465,"key":"Guardian","name":"Guardian","shortDesc":"Guard allies you cast spells on and those that are very nearby. If you or a guarded ally would take damage, you're both hasted and granted a shield.","longDesc":"<i>Guard</i> allies within @SnuggleRange@ units of you, and allies you target with spells for @GuardDuration@s. While <i>Guarding</i>, if you or the ally take damage, both of you gain a shield and are hasted for @ShieldDuration@s.<br><br>Cooldown: <scaleLevel>@Cooldown@ - @CooldownMaxLevel@</scaleLevel> seconds<br>Shield: <scaleLevel>@ShieldBase@ - @ShieldMax@</scaleLevel> + <scaleAP>@APRatio.-1@%</scaleAP> of your ability power + <scalehealth>@HPRatio.0*100@%</scalehealth> of your bonus health.<br>Haste: +@Haste*100@% Movement Speed.","icon":"ASSETS/Perks/Styles/Resolve/Guardian/Guardian.dds","runePathId":8400,"runePathName":"Resolve"},{"id":8143,"key":"SuddenImpact","name":"Sudden Impact","shortDesc":"Gain a burst of Lethality and Magic Penetration after using a dash, leap, blink, teleport, or when leaving stealth.","longDesc":"After exiting stealth or using a dash, leap, blink, or teleport, dealing any damage to a champion grants you @BonusLethality.0@ Lethality and @BonusMpen.0@ Magic Penetration for @Duration@s.<br><br>Cooldown: @Cooldown@s","icon":"ASSETS/Perks/Styles/Domination/SuddenImpact/SuddenImpact.dds","runePathId":8100,"runePathName":"Domination"},{"id":9111,"key":"Triumph","name":"Triumph","shortDesc":"<lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Takedown'>Takedowns</lol-uikit-tooltipped-keyword> restore @MissingHealthRestored.0*100@% of your missing health and grant an additional @BonusGold@ gold. ","longDesc":"Takedowns restore @MissingHealthRestored.0*100@% of your missing health and grant an additional @BonusGold@ gold. <br><br><hr></hr><br><i>'The most dangerous game brings the greatest glory.' <br>—Noxian Reckoner</i>","icon":"ASSETS/Perks/Styles/Precision/DangerousGame.dds","runePathId":8000,"runePathName":"Precision"},{"id":8463,"key":"FontOfLife","name":"Font of Life","shortDesc":"<lol-uikit-tooltipped-keyword key='LinkTooltip_Description_ImpairMov'>Impairing</lol-uikit-tooltipped-keyword> the movement of an enemy champion marks them. Your allies heal when attacking champions you've marked. ","longDesc":"Impairing the movement of an enemy champion marks them for @MarkDuration@s.<br><br>Ally champions who attack marked enemies heal for @FlatHealAmount@ + @HealthRatio.-1 * 100@% of your max health over @HealDuration@s. ","icon":"ASSETS/Perks/Styles/Resolve/FontOfLife/FontOfLife.dds","runePathId":8400,"runePathName":"Resolve"},{"id":8105,"key":"RelentlessHunter","name":"Relentless Hunter","shortDesc":"<b>Unique</b> <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Takedown'>takedowns</lol-uikit-tooltipped-keyword> grant permanent <b>out of combat <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_MS'>MS</lol-uikit-tooltipped-keyword></b>. ","longDesc":"Gain @StartingOOCMS@ <b>out of combat Movement Speed</b> plus @OOCMS.0@ per <i>Bounty Hunter</i> stack.<br><br>Earn a <i>Bounty Hunter</i> stack the first time you get a takedown on each enemy champion.","icon":"ASSETS/Perks/Styles/Domination/RelentlessHunter/RelentlessHunter.dds","runePathId":8100,"runePathName":"Domination"},{"id":8347,"key":"CosmicInsight","name":"Cosmic Insight","shortDesc":"+@CDR*100@% <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_CDR'>CDR</lol-uikit-tooltipped-keyword><br>+@CDR*100@% Max CDR<br>+@CDR*100@% Summoner Spell CDR<br>+@CDR*100@% Item CDR","longDesc":"+@CDR*100@% CDR<br>+@CDR*100@% Max CDR<br>+@CDR*100@% Summoner Spell CDR<br>+@CDR*100@% Item CDR","icon":"ASSETS/Perks/Styles/Inspiration/CosmicInsight/CosmicInsight.dds","runePathId":8300,"runePathName":"Inspiration"},{"id":8226,"key":"ManaflowBand","name":"Manaflow Band","shortDesc":"Hitting an enemy champion with an ability permanently increases your maximum mana by @ManaIncrease@, up to @MaxManaIncrease@ mana.<br><br>After reaching @MaxManaIncrease@ bonus mana, restore @PercentManaRestore*100@% of your missing mana every @PercentManaRestoreCooldown@ seconds.","longDesc":"Hitting an enemy champion with an ability permanently increases your maximum mana by @ManaIncrease@, up to @MaxManaIncrease@ mana.<br><br>After reaching @MaxManaIncrease@ bonus mana, restore @PercentManaRestore*100@% of your missing mana every @PercentManaRestoreCooldown@ seconds.<br><br>Cooldown: @Cooldown.0@ seconds","icon":"ASSETS/Perks/Styles/Sorcery/ManaflowBand/ManaflowBand.dds","runePathId":8200,"runePathName":"Sorcery"},{"id":8304,"key":"MagicalFootwear","name":"Magical Footwear","shortDesc":"You get free boots at @GiveBootsAtMinute@ min but you cannot buy boots before then. Each <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Takedown'>takedown</lol-uikit-tooltipped-keyword> you get makes your boots come @SecondsSoonerPerTakedown@s sooner.","longDesc":"You get free Slightly Magical Boots at @GiveBootsAtMinute@ min, but you cannot buy boots before then. For each takedown you acquire the boots @SecondsSoonerPerTakedown@s sooner.<br><br>Slightly Magical Boots give you an additional +@AdditionalMovementSpeed@ Movement Speed.","icon":"ASSETS/Perks/Styles/Inspiration/MagicalFootwear/MagicalFootwear.dds","runePathId":8300,"runePathName":"Inspiration"},{"id":8345,"key":"BiscuitDelivery","name":"Biscuit Delivery","shortDesc":"Gain a free Biscuit every @BiscuitMinuteInterval@ min, until @SwapOverMinute@ min. Consuming a Biscuit permanently increases your max mana and restores health and mana.","longDesc":"Biscuit Delivery: Gain a Total Biscuit of Everlasting Will every @BiscuitMinuteInterval@ mins, until @SwapOverMinute@ min.<br><br>Biscuits restore @HealthHealPercent.0*100@% of your missing health and mana. Consuming any Biscuit increases your mana cap by @PermanentMana@ mana permanently. <br><br><i>Manaless:</i> Champions without mana restore @HealthHealPercentManaless.0*100@% missing health instead.","icon":"ASSETS/Perks/Styles/Inspiration/BiscuitDelivery/BiscuitDelivery.dds","runePathId":8300,"runePathName":"Inspiration"},{"id":8224,"key":"NullifyingOrb","name":"Nullifying Orb","shortDesc":"Gain a magic damage shield when taken to low health by magic damage.","longDesc":"When you take magic damage that would reduce your Health below @PercHealthTrigger.0*100@%, gain a shield that absorbs @ShieldMin@ - @ShieldMax@ magic damage based on level (<scaleAP>+@APRatio.-1@ AP</scaleAP> and <scaleAD>+@ADRatio.-1@ bonus AD</scaleAD>) for @ShieldDuration@s.<br><br>Cooldown: @Cooldown@s","icon":"ASSETS/Perks/Styles/Sorcery/NullifyingOrb/Pokeshield.dds","runePathId":8200,"runePathName":"Sorcery"},{"id":8021,"key":"FleetFootwork","name":"Fleet Footwork","shortDesc":"Attacking and moving builds Energy stacks. At 100 stacks, your next attack heals you and grants increased <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_MS'>MS</lol-uikit-tooltipped-keyword>.","longDesc":"Attacking and moving builds Energy stacks. At 100 stacks, your next attack is Energized.<br><br>Energized attacks heal you for @HealBase@ - @HealMax@ (+@HealBonusADRatio.-1@ Bonus AD, +@HealAPRatio.-1@ AP) and grant +@MSBuff*100@% movement speed for @MSDuration.0@s.<br><rules>Healing is @MinionHealMod*100@% as effective when used on a minion (@MinionHealMod*50@% effective for ranged).<br>Healing is increased by @HealCritMod*100@% of your critical damage modifier when triggered by a critical hit.</rules>","icon":"ASSETS/Perks/Styles/Precision/FleetFootwork/FleetFootwork.dds","runePathId":8000,"runePathName":"Precision"},{"id":8112,"key":"Electrocute","name":"Electrocute","shortDesc":"Hitting a champion with 3 <b>separate</b> attacks or abilities in @WindowDuration@s deals bonus <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_AdaptiveDmg'>adaptive damage</lol-uikit-tooltipped-keyword>.","longDesc":"Hitting a champion with 3 <b>separate</b> attacks or abilities within @WindowDuration@s deals bonus <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_AdaptiveDmg'><font color='#48C4B7'>adaptive damage</font></lol-uikit-tooltipped-keyword>.<br><br>Damage: @DamageBase@ - @DamageMax@ (+@BonusADRatio.-1@ bonus AD, +@APRatio.-1@ AP) damage.<br><br>Cooldown: @Cooldown@ - @CooldownMin@s<br><br><hr></hr><i>'We called them the Thunderlords, for to speak of their lightning was to invite disaster.'</i>","icon":"ASSETS/Perks/Styles/Domination/Electrocute/Electrocute.dds","runePathId":8100,"runePathName":"Domination"},{"id":8233,"key":"AbsoluteFocus","name":"Absolute Focus","shortDesc":"While above @HealthPercent*100@% health, gain extra <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_AdaptiveDmg'>adaptive damage</lol-uikit-tooltipped-keyword>.","longDesc":"While above @HealthPercent*100@% health, gain an <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'><font color='#48C4B7'>adaptive</font></lol-uikit-tooltipped-keyword> bonus of up to @MaxAdaptive.-1*0.6@ Attack Damage or @MaxAdaptive@ Ability Power (based on level). <br><br>Grants @MinAdaptive.-1*0.6@ Attack Damage or @MinAdaptive@ Ability Power at level 1. ","icon":"ASSETS/Perks/Styles/Sorcery/AbsoluteFocus/AbsoluteFocus.dds","runePathId":8200,"runePathName":"Sorcery"},{"id":8234,"key":"Celerity","name":"Celerity","shortDesc":"Gain @PercentMS.0@% extra <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_MS'>MS</lol-uikit-tooltipped-keyword>. Gain extra AP or AD, <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'>adaptive</lol-uikit-tooltipped-keyword> based on your bonus MS. ","longDesc":"Gain @PercentMS.0@% increased Movement Speed.<br>Your Bonus Movement Speed is converted to Attack Damage or Ability Power, <font color='#48C4B7'>adaptive</font> at a rate of @AdaptiveAD*8@% Attack Damage or @AdaptiveAP*8@% Ability Power.","icon":"ASSETS/Perks/Styles/Sorcery/Celerity/CelerityTemp.dds","runePathId":8200,"runePathName":"Sorcery"},{"id":8352,"key":"TimeWarpTonic","name":"Time Warp Tonic","shortDesc":"Your potions, biscuits and elixirs last @PotionDuration*100@% longer, and you gain @BonusMS*100@% Movement Speed while under their effects.","longDesc":"Your potions, biscuits and elixirs last @PotionDuration*100@% longer, and you gain @BonusMS*100@% Movement Speed while under their effects.","icon":"ASSETS/Perks/Styles/Inspiration/TimeWarpTonic/TimeWarpTonic.dds","runePathId":8300,"runePathName":"Inspiration"},{"id":8473,"key":"BonePlating","name":"Bone Plating","shortDesc":"After taking damage from an enemy champion, the next @BlockCount@ spells or attacks you receive from them deal @BlockBase@-@BlockMax@ less damage.<br><br>Duration: @BlockDuration@s<br>Cooldown: @Cooldown@s","longDesc":"After taking damage from an enemy champion, the next @BlockCount@ spells or attacks you receive from them deal @BlockBase@-@BlockMax@ less damage.<br><br>Duration: @BlockDuration@s<br>Cooldown: @Cooldown@s","icon":"ASSETS/Perks/Styles/Resolve/BonePlating/BonePlating.dds","runePathId":8400,"runePathName":"Resolve"},{"id":8232,"key":"Waterwalking","name":"Waterwalking","shortDesc":"Gain <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_MS'>MS</lol-uikit-tooltipped-keyword> and AP or AD, <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'>adaptive</lol-uikit-tooltipped-keyword> in the river.","longDesc":"Gain @MovementSpeed@ Movement Speed and an <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'><font color='#48C4B7'>adaptive</font></lol-uikit-tooltipped-keyword> bonus of up to @MaxAdaptive.-1*0.6@ Attack Damage or @MaxAdaptive@ Ability Power (based on level) when in the river.<br><br><hr></hr><br><i>May you be as swift as the rushing river and agile as a startled Rift Scuttler.</i><br>","icon":"ASSETS/Perks/Styles/Sorcery/Waterwalking/Waterwalking.dds","runePathId":8200,"runePathName":"Sorcery"},{"id":8237,"key":"Scorch","name":"Scorch","shortDesc":"Your first ability hit every @BurnlockoutDuration@s burns champions.","longDesc":"Your next ability hit sets champions on fire dealing @damage@ - @damagemax@ bonus magic damage based on level after @dotduration@s.<br><br>Cooldown: @BurnlockoutDuration@s","icon":"ASSETS/Perks/Styles/Sorcery/Scorch/Scorch.dds","runePathId":8200,"runePathName":"Sorcery"},{"id":8359,"key":"Kleptomancy","name":"Kleptomancy","shortDesc":"After using an ability, your next attack will grant bonus gold if used on a champion. There's a chance you'll also gain a consumable.","longDesc":"After using an ability, your next attack will grant bonus gold if used on a champion. There's a chance you'll also gain a consumable.","icon":"ASSETS/Perks/Styles/Inspiration/Kleptomancy/Kleptomancy.dds","runePathId":8300,"runePathName":"Inspiration"},{"id":8313,"key":"PerfectTiming","name":"Perfect Timing","shortDesc":"Gain a free Stopwatch. Stopwatch has a one time use <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Stasis'>Stasis</lol-uikit-tooltipped-keyword> effect.","longDesc":"Start the game with a Commencing Stopwatch that transforms into a Stopwatch after @InitialCooldown.0@ min. Stopwatch has a one time use Stasis effect.<br><br>Reduces the cooldown of Zhonya's Hourglass, Guardian Angel, and Gargoyle Stoneplate by @PercentGAZhonyasCDR.0*100@%.","icon":"ASSETS/Perks/Styles/Inspiration/PerfectTiming/PerfectTiming.dds","runePathId":8300,"runePathName":"Inspiration"},{"id":8236,"key":"GatheringStorm","name":"Gathering Storm","shortDesc":"Gain increasing amounts of AD or AP, <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'>adaptive</lol-uikit-tooltipped-keyword> over the course of the game.","longDesc":"Every @UpdateAfterMinutes@ min gain AP or AD, <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'><font color='#48C4B7'>adaptive</font></lol-uikit-tooltipped-keyword>.<br><br><i>10 min</i>: + 8 AP or 5 AD <br><i>20 min</i>: + 24 AP or 14 AD<br><i>30 min</i>: + 48 AP or 29 AD<br><i>40 min</i>: + 80 AP or 48 AD<br><i>50 min</i>: + 120 AP or 72 AD<br><i>60 min</i>: + 168 AP or 101 AD<br>etc...","icon":"ASSETS/Perks/Styles/Sorcery/GatheringStorm/GatheringStorm.dds","runePathId":8200,"runePathName":"Sorcery"},{"id":8351,"key":"GlacialAugment","name":"Glacial Augment","shortDesc":"Your first attack against an enemy champion slows them (per unit cooldown). Slowing champions with active items shoots a freeze ray at them, creating a lingering slow zone.","longDesc":"Basic attacking a champion slows them for @SlowDuration.0@s. The slow increases in strength over its duration.<li><i>Ranged</i>: Ranged attacks slow by up to @SlowAmountBase.0*-100@% - @SlowAmountMax.0*-100@%</li> <li><i>Melee</i>: Melee attacks slow by up to @SlowAmountBaseMelee.0*-100@% - @SlowAmountMaxMelee.0*-100@%</li><br>Slowing a champion with active items shoots a freeze ray through them, freezing the nearby ground for @SlowZoneDuration@s, slowing all units inside by @SlowZoneSlow*-100@%.<br><br>Cooldown: @UnitCDBase@-@UnitCD16@s per unit","icon":"ASSETS/Perks/Styles/Inspiration/GlacialAugment/GlacialAugment.dds","runePathId":8300,"runePathName":"Inspiration"},{"id":8472,"key":"Chrysalis","name":"Chrysalis","shortDesc":"Start the game with an extra @StartingHealth@ health. At @MaxTakedowns@ takedowns, consume that health to gain an <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'><font color='#48C4B7'>adaptive</font></lol-uikit-tooltipped-keyword> bonus of @AdaptiveForce.-1*0.6@ Attack Damage or @AdaptiveForce@ Ability Power.","longDesc":"Start the game with an extra @StartingHealth@ health. At @MaxTakedowns@ takedowns, consume that health to gain an <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Adaptive'><font color='#48C4B7'>adaptive</font></lol-uikit-tooltipped-keyword> bonus of @AdaptiveForce.-1*0.6@ Attack Damage or @AdaptiveForce@ Ability Power.","icon":"ASSETS/Perks/Styles/Resolve/Chrysalis/Chrysalis.dds","runePathId":8400,"runePathName":"Resolve"},{"id":8230,"key":"PhaseRush","name":"Phase Rush","shortDesc":"Hitting an enemy champion with 3 <b>separate</b> attacks or abilities grants a burst of <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_MS'>MS</lol-uikit-tooltipped-keyword>. ","longDesc":"Hitting an enemy champion with 3 attacks or <b>separate</b> abilities within @Window@s grants @HasteBase*100@ - @HasteMax*100@% Movement Speed based on level and @SlowResist*100@% Slow Resistance.<br><br>Duration: @Duration@s<br>Cooldown: @Cooldown@s","icon":"ASSETS/Perks/Styles/Sorcery/PhaseRush/PhaseRush.dds","runePathId":8200,"runePathName":"Sorcery"},{"id":8429,"key":"Conditioning","name":"Conditioning","shortDesc":"After @MinutesRequired@ min gain +@ArmorBase@ Armor and +@MRBase@ Magic Resist and increase your Armor and Magic Resist by @ExtraResist@%.","longDesc":"After @MinutesRequired@ min gain +@ArmorBase@ Armor and +@MRBase@ Magic Resist and increase your Armor and Magic Resist by @ExtraResist@%.","icon":"ASSETS/Perks/Styles/Resolve/Conditioning/Conditioning.dds","runePathId":8400,"runePathName":"Resolve"},{"id":8306,"key":"HextechFlashtraption","name":"Hextech Flashtraption","shortDesc":"While Flash is on cooldown it is replaced by <i>Hexflash</i>.<br><br><i>Hexflash</i>: Channel, then blink to a new location.","longDesc":"While Flash is on cooldown it is replaced by <i>Hexflash</i>.<br><br><i>Hexflash</i>: Channel for @ChannelDuration@s to blink to a new location.<br><br>Cooldown: @CooldownTime@s. Goes on a @ChampionCombatCooldown@s cooldown when you enter champion combat.","icon":"ASSETS/Perks/Styles/Inspiration/HextechFlashtraption/HextechFlashtraption.dds","runePathId":8300,"runePathName":"Inspiration"},{"id":8229,"key":"ArcaneComet","name":"Arcane Comet","shortDesc":"Damaging a champion with an ability hurls a damaging comet at their location.","longDesc":"Damaging a champion with an ability hurls a comet at their location, or, if Arcane Comet is on cooldown, reduces its remaining cooldown.<br><br><lol-uikit-tooltipped-keyword key='LinkTooltip_Description_AdaptiveDmg'><font color='#48C4B7'>Adaptive Damage</font></lol-uikit-tooltipped-keyword>: @DamageBase@ - @DamageMax@ based on level (<scaleAP>+@APRatio.-1@ AP</scaleAP> and <scaleAD>+@ADRatio.-1@ bonus AD</scaleAD>)<br>Cooldown: @RechargeTime@ - @RechargeTimeMin@s<br><rules><br>Cooldown Reduction:<br>Single Target: @PercentRefund*100@%.<br>Area of Effect: @AoEPercentRefund*100@%.<br>Damage over Time: @DotPercentRefund*100@%.<br></rules>","icon":"ASSETS/Perks/Styles/Sorcery/ArcaneComet/ArcaneComet.dds","runePathId":8200,"runePathName":"Sorcery"},{"id":8321,"key":"FuturesMarket","name":"Future's Market","shortDesc":"You can enter debt to buy items.","longDesc":"You can enter debt to buy items. The amount you can borrow increases over time.<br><br>Lending Fee: @ExcessCostPenaltyFlat@ gold","icon":"ASSETS/Perks/Styles/Inspiration/FuturesMarket/FuturesMarket.dds","runePathId":8300,"runePathName":"Inspiration"},{"id":8124,"key":"Predator","name":"Predator","shortDesc":"Add an active effect to your boots that grants a large boost of <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_MS'>MS</lol-uikit-tooltipped-keyword> and causes your next attack or ability to deal bonus <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_AdaptiveDmg'>adaptive damage</lol-uikit-tooltipped-keyword>.","longDesc":"Enchants your boots with the active effect '<font color='#c60300'>Predator</font>.'<br><br>Channel for 1.5s out of combat to gain 45% movement speed for 15s. Damaging attacks or abilities end this effect, dealing 60 - 180 (+<scaleAD>0.4</scaleAD> bonus AD)(+<scaleAP>0.25</scaleAP> AP) bonus <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_AdaptiveDmg'><font color='#48C4B7'>adaptive damage</font></lol-uikit-tooltipped-keyword>.<br><br>Cooldown: 150s - 100s. Starts the game on cooldown. 50% cooldown if interrupted while channeling.","icon":"ASSETS/Perks/Styles/Domination/Predator/Predator.dds","runePathId":8100,"runePathName":"Domination"},{"id":8242,"key":"Unflinching","name":"Unflinching","shortDesc":"After casting a Summoner Spell, gain Tenacity and Slow Resistance for a short duration. Additionally, gain Tenacity and Slow Resistance for each Summoner Spell on cooldown. ","longDesc":"After casting a Summoner Spell, gain @BonusTenacity*100@% Tenacity and Slow Resistance for @BuffDuration@s. Additionally, gain @PersistTenacity*100@% Tenacity and Slow Resistance for each Summoner Spell on cooldown. ","icon":"ASSETS/Perks/Styles/Sorcery/Unflinching/Unflinching.dds","runePathId":8400,"runePathName":"Resolve"},{"id":8243,"key":"TheUltimateHat","name":"The Ultimate Hat","shortDesc":"Your ultimate's cooldown is reduced. Each time you cast your ultimate, its cooldown is further reduced.","longDesc":"Your ultimate's cooldown is reduced by @StartingCDR@%. Each time you cast your ultimate, its cooldown is further reduced by @CDChunkPerStack@%. Stacks up to @MaxStacks@ times.","icon":"ASSETS/Perks/Styles/Sorcery/TheUltimateHat/TheUltimateHat.dds","runePathId":8200,"runePathName":"Sorcery"},{"id":8446,"key":"Demolish","name":"Demolish","shortDesc":"Charge up a powerful attack against a tower while near it.","longDesc":"Charge up a powerful attack against a tower over @TotalDemolishTime@s, while within @DistanceToTower@ range of it. The charged attack deals @OutputDamagePerStack@ (+@MaxHealthPercentDamage.0 * 100@% of your max health) bonus physical damage.<br><br>Cooldown: @CooldownSeconds@s","icon":"ASSETS/Perks/Styles/Resolve/Demolish/Demolish.dds","runePathId":8400,"runePathName":"Resolve"},{"id":8128,"key":"DarkHarvest","name":"Dark Harvest","shortDesc":"Champions, large minions, and large monsters drop soul essence on death. Touch souls to absorb them and deal bonus <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_AdaptiveDmg'>adaptive damage</lol-uikit-tooltipped-keyword> on your next attack based on total soul essence collected.","longDesc":"Champions, large minions, and large monsters drop soul essence on death. Collect souls to become <font color='#c60300'>Soul Charged</font>. Your next attack on a champion or structure consumes <font color='#c60300'>Soul Charged</font> to deal bonus <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_AdaptiveDmg'><font color='#48C4B7'>adaptive damage</font></lol-uikit-tooltipped-keyword>.<br><br><font color='#c60300'>Soul Charged</font> lasts @ONHDuration@s, increased to @ONHDurationLong@s after collecting @SoulsRequiredForIncreasedDuration@ soul essence.<br><br>Bonus damage: @DamageMin@ - @DamageMax@ (+<scaleAD>@ADRatio.2@ bonus AD</scaleAD>) (+<scaleAP>@APRatio.1@ AP</scaleAP>) + soul essence collected.<br><rules><br>Champions - @champstacks@ soul essence.<br>Monsters - @monsterstacks@ soul essence.<br>Minions - @minionstacks@ soul essence.</rules>","icon":"ASSETS/Perks/Styles/Domination/DarkHarvest/DarkHarvest.dds","runePathId":8100,"runePathName":"Domination"},{"id":8326,"key":"UnsealedSpellbook","name":"Unsealed Spellbook","shortDesc":"Exchange Summoner Shards at the shop to change your Summoner Spells during game. Your Summoner Spells have reduced cooldowns. <br>","longDesc":"Gain a Summoner Shard at @ShardFirstMinutes@ min and another every @ShardRechargeMinutes@ min after (Max @Maxshards@ shards).<br><br>While near the shop, you can exchange @ShardCost@ Summoner Shard to replace a Summoner Spell with a different one. <br><br>Additionally, your Summoner Spell Cooldowns are reduced by @SummonerCDR.0*100@%.<br><br><rules><i>Smite:</i> Buying Smite won't grant access to Smite items<br>You cannot have two of the same Summoner Spell</rules>","icon":"ASSETS/Perks/Styles/Inspiration/UnsealedSpellbook/UnsealedSpellbook.dds","runePathId":8300,"runePathName":"Inspiration"},{"id":8444,"key":"SecondWind","name":"Second Wind","shortDesc":"After taking damage from an enemy champion heal back some missing health over time. ","longDesc":"After taking damage from an enemy champion, heal for @RegenPercentMax.0*100@% of your missing health +@RegenFlat.0@ over @RegenSeconds@s.","icon":"ASSETS/Perks/Styles/Resolve/SecondWind/SecondWind.dds","runePathId":8400,"runePathName":"Resolve"},{"id":8126,"key":"CheapShot","name":"Cheap Shot","shortDesc":"Deal bonus true damage to enemy champions with <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_ImpairAct'>impaired movement or actions</lol-uikit-tooltipped-keyword>. ","longDesc":"Damaging champions with <b>impaired movement or actions</b> deals @DamageIncMin@ - @DamageIncMax@ bonus true damage (based on level).<br><br>Cooldown: @Cooldown@s<br><rules>Activates on damage occurring after the impairment.</rules>","icon":"ASSETS/Perks/Styles/Domination/CheapShot/CheapShot.dds","runePathId":8100,"runePathName":"Domination"},{"id":8005,"key":"PressTheAttack","name":"Press the Attack","shortDesc":"Hitting an enemy champion @HitsRequired@ consecutive times makes them vulnerable, dealing bonus damage and causing them to take more damage from all sources for @AmpDuration@s.","longDesc":"Hitting an enemy champion with @HitsRequired@ consecutive basic attacks deals @MinDamage@ - @MaxDamage@ bonus <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_AdaptiveDmg'><font color='#48C4B7'>adaptive damage</font></lol-uikit-tooltipped-keyword> (based on level) and makes them vulnerable, increasing the damage they take by @AmpPotencyStartSelf.0*100@ - @AmpPotencyMaxSelf.0*100@% from all sources for @AmpDuration@s.","icon":"ASSETS/Perks/Styles/Precision/PressTheAttack/PressTheAttack.dds","runePathId":8000,"runePathName":"Precision"},{"id":8120,"key":"GhostPoro","name":"Ghost Poro","shortDesc":"When you enter brush, a poro appears. It will stay behind to give you vision.","longDesc":"Enter a brush to summon a poro after a brief channel. The poro will stay behind to give you vision until you summon a new one.<br><br>If an enemy enters brush with a poro in it, they scare it away, putting Ghost Poro on a @Cooldown@s cooldown.<br><br>Poro channel is interrupted if you take damage.","icon":"ASSETS/Perks/Styles/Domination/GhostPoro/GhostPoro.dds","runePathId":8100,"runePathName":"Domination"},{"id":8439,"key":"Aftershock","name":"Aftershock","shortDesc":"After <lol-uikit-tooltipped-keyword key='LinkTooltip_Description_Immobilize'>immobilizing</lol-uikit-tooltipped-keyword> an enemy champion gain defenses and later deal a burst of magic damage around you.","longDesc":"After immobilizing an enemy champion, increase your Armor and Magic Resist by @FlatResists@ - @FlatResistMaximum@ for @DelayBeforeBurst.1@s. Then explode, dealing magic damage to nearby enemies.<br><br>Damage: @StartingBaseDamage@ - @MaxBaseDamage@ (+@HealthRatio.-1@% of your maximum health) (+@DamageRatioAD*100@% of your bonus attack damage) (+@DamageRatioAP*100@% of your ability power)<br>Cooldown: @Cooldown@s","icon":"ASSETS/Perks/Styles/Resolve/VeteranAftershock/VeteranAftershock.dds","runePathId":8400,"runePathName":"Resolve"},{"id":8316,"key":"MinionDematerializer","name":"Minion Dematerializer","shortDesc":"Start the game with @GainedMinionKillers@ Minion Dematerializers. Killing minions with the item gives permanent bonus damage vs. that minion type.","longDesc":"Start the game with @GainedMinionKillers@ Minion Dematerializers that kill and absorb lane minions instantly. Minion Dematerializers are on cooldown for the first @InitialCooldown@s of the game.<br><br>Absorbing a minion increases your damage by +@DamageBonusForAnyAbsorbed.0*100@% against that type of minion permanently, and an extra +@DamageBonusPerAdditionalAbsorbed.0*100@% for each additional minion of that type absorbed.<br>","icon":"ASSETS/Perks/Styles/Inspiration/MinionDematerializer/MinionDematerializer.dds","runePathId":8300,"runePathName":"Inspiration"},{"id":8437,"key":"GraspOfTheUndying","name":"Grasp of the Undying","shortDesc":"Every @TriggerTime@s your next attack on a champion deals bonus magic damage, heals you, and permanently increases your health.","longDesc":"Every @TriggerTime@s in combat, your next basic attack on a champion will:<li>Deal bonus magic damage equal to @PercentHealthDamage.0@% of your max health</li><li>Heals you for @PercentHealthHeal.0*100@% of your max health</li><li>Permanently increase your health by @MaxHealthPerProc@</li><br><rules><i>Ranged Champions:</i> Damage, healing, and permanent health gained reduced by @RangedPenaltyMod*100@%.</rules><br>","icon":"ASSETS/Perks/Styles/Resolve/GraspOfTheUndying/GraspOfTheUndying.dds","runePathId":8400,"runePathName":"Resolve"}]
class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html', context=None)
	def post(self, request, **kwargs):
		pass
class Stats:
	def __init__(self,league,tier,lp,winsLosses,winRatio,hotStreak):
		self.league = league
		self.tier = tier
		self.lp = lp
		self.winsLosses = winsLosses
		self.winRatio = winRatio
		self.hotStreak = False

"""
This is the function that will be ran when the user enters the /signup/ page.
It will load up the SignUpForm in the forms.py file and then check if the user credentials are valid.
It will then authenticate the user(logging them into the website) and then save the information in the database.
"""
def mySignup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			print(username)
			print(raw_password)
			user = authenticate(username=username, password=raw_password)
			print(user)
			login(request, user)
			return redirect('home')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})
"""
This function will be ran when the user presses the logout button, which will then use the built in django log out system to log them out
of the website and then redirect them to the home page.
"""
def myLogout(request):
	logout(request)
	return redirect('home')
def set_password(self, UnsafePassword):
	pubKey = "2257, 47"
	encryptedPassword = (encrypt(UnsafePassword, pubKey))
	#uses RSA encryption to encrypt the password
	self.password = encryptedPassword

def myLogin(request):
	pubKey = "2257, 47"
	if request.method == 'POST':
		username = request.POST.get('username')
		raw_password = request.POST.get('psw')
		user = authenticate(username=username, password=raw_password)
		if user == None:
			return redirect('home')
		else:
			login(request, user)
		return redirect('home')
"""
This class is used to store the information of a given summoner name, which will be used in app.html to present their statistics such as
amount of ranked games won.
"""


"""
This is a class that will instantiated during run time and will become an object when instantiated.
It contains all the information that will be needed when displaying information from a specific match when a summoner's name has been searched.
It will contain it's on API calls, to the match endpoint, to get obtain that further information, which will be sorted and saved as variables.
"""
class Participant:
	def __init__(self,account_id,summonerName,champion_id):
		pass
class Match:
	def __init__(self, gameInfo, accountID, summonerID, summonerName, key):
		region = 'euw1'
		self.accountID = accountID
		self.summonerID = summonerID
		self.summonerName = summonerName
		self.game = gameInfo
		self.timestamp = self.game['timestamp']
		self.gameID = self.game['gameId']
		self.role = self.game['role']
		self.lane = self.game['lane']
		self.championID = self.game['champion']
		match= key.match.by_id(region, self.gameID)

		self.queueType = match['queueId']
		self.queueID = self.queueType
		self.queueType = queues[int(self.queueID)][1]
		self.queueMap = queues[self.queueID][0]
		"""
		The for loop below loops through the participants in the http request to find the id of the summoner being searched for.

		Once a summoner is found, it will load up the individual stats for the summoner in the variable defined as stats
		"""
		
		self.durationSeconds = match['gameDuration']
		self.durationMinutes = int(self.durationSeconds) // 60
		self.duration = time.strftime("%M:%S", time.gmtime(self.durationSeconds))

		self.participants = []
		for player in match['participantIdentities']:
			data = player['player']
			participantID = player['participantId']
			participant = match['participants'][participantID-1]
			summonerName = player['player']['summonerName']				
			if player['player']['accountId'] == accountID or player['player']['currentAccountId'] == accountID:
				self.player = Player(self.durationMinutes,participant, summonerName)
			self.participants.append(Player(self.durationMinutes,participant, summonerName))
		

		


class Player():
	def __init__(self,durationMinutes,participant, summonerName):
		stats = participant['stats']
		self.win = stats['win']
		if self.win:
			self.win = 'Victory'
		else:
			self.win = 'Defeat'
		champ = Champion.objects.get(champion_id=participant['championId'])
		self.champPhoto = champ.image
		self.champName = champ.name
		self.summonerName = summonerName
		self.spell_1 = Spell.objects.get(spellID=participant['spell1Id'])
		self.spell_2 = Spell.objects.get(spellID=participant['spell2Id'])
		self.KDA = "%s/%s/%s"%(stats['kills'],stats['deaths'],stats['assists'])
		if stats['deaths'] != 0:
			self.KDA_ratio = (stats['assists'] + stats['kills']) / stats['deaths']
		self.preLevel = stats['champLevel']
		self.level = 'Level' + str(self.preLevel)
		self.baseCs = stats['totalMinionsKilled']
		self.csPerMin = int(self.baseCs) / durationMinutes
		self.csPerMin = "%.2f" % self.csPerMin
		self.cs = str(self.baseCs) + ' (%s) cs' %(self.csPerMin)
		self.spell_2_image = self.spell_2.image
		self.spell_1_image = self.spell_1.image
		self.rune_main_1_id = stats['perk0']
		self.rune_main_2_id = stats['perk1']
		self.rune_main_3_id = stats['perk2']
		self.rune_main_4_id = stats['perk3']
		self.rune_secondary_1_id = stats['perk4']
		self.rune_secondary_2_id = stats['perk5']
		self.rune_main_style_id = stats['perkPrimaryStyle']
		self.rune_secondary_style_id = stats['perkSubStyle']
		self.runePrefix = 'http://stelar7.no/cdragon/latest/perks'
		self.rune_main_1_icon = self.runePrefix + "/" + str(self.rune_main_1_id) +'.png'
		self.rune_main_2_icon = self.runePrefix + "/" + str(self.rune_main_2_id) +'.png'
		self.rune_main_3_icon = self.runePrefix + "/" + str(self.rune_main_3_id) +'.png'
		self.rune_main_4_icon = self.runePrefix + "/" + str(self.rune_main_4_id) +'.png'
		self.rune_secondary_1_icon = self.runePrefix + "/" + str(self.rune_secondary_1_id) +'.png'
		self.rune_secondary_2_icon = self.runePrefix + "/" + str(self.rune_secondary_2_id) +'.png'
		self.rune_main_style_icon = self.runePrefix + 'tyles/' + str(self.rune_main_style_id) +'.png'
		self.rune_secondary_style_icon = self.runePrefix + 'tyles/' + str(self.rune_secondary_style_id) +'.png'
		# self.item_1_id = stats['item1']
		# self.item_2_id = stats['item2']
		# self.item_3_id = stats['item3']
		# self.item_4_id = stats['item4']
		# self.item_5_id = stats['item5']
		self.item_ids = []
		self.item_images = []
		for i in range(6):
			self.item_ids.append(stats['item' + str(i)])
			self.item_images.append('http://stelar7.no/cdragon/latest/items/' + str(self.item_ids[i]) + '.png')
		# self.item_1_image = 'http://stelar7.no/cdragon/latest/items/' + str(self.item_1_id) + '.png'
		# self.item_2_image = 'http://stelar7.no/cdragon/latest/items/' + str(self.item_2_id) + '.png'
		# self.item_3_image = 'http://stelar7.no/cdragon/latest/items/' + str(self.item_3_id) + '.png'
		# self.item_4_image = 'http://stelar7.no/cdragon/latest/items/' + str(self.item_4_id) + '.png'
		# self.item_5_image = 'http://stelar7.no/cdragon/latest/items/' + str(self.item_5_id) + '.png'

		for rune in runes:
			if rune['id'] == self.rune_main_1_id:
				self.rune_main_1 = rune['name']
				self.rune_main_1_description = rune['shortDesc']
				self.rune_main_style = rune['runePathName']
			elif rune['id'] == self.rune_main_2_id:
				self.rune_main_2 = rune['name']
				self.rune_main_2_description = rune['shortDesc']
			elif rune['id'] == self.rune_main_3_id:
				self.rune_main_3 = rune['name']
				self.rune_main_3_description = rune['shortDesc']
			elif rune['id'] == self.rune_main_4_id:
				self.rune_main_4 = rune['name']
				self.rune_main_4_description = rune['shortDesc']
			elif rune['id'] == self.rune_secondary_1_id:
				self.rune_secondary_1 = rune['name']
				self.rune_secondary_1_desc = rune['shortDesc']
				self.rune_secondary_style = rune['runePathName']
			elif rune['id'] == self.rune_secondary_2_id:
				self.rune_secondary_2 = rune['name']
				self.rune_secondary_2_desc = rune['shortDesc']

"""
                "item2": 1402,
                "item3": 3020,
                "item0": 3157,
                "item1": 3102,
                "item6": 3340,
                "item4": 3165,
                "item5": 3100,
"""	
class app(TemplateView):
	template_name = 'app.html'
class mySearch(TemplateView):


	def displayStats(stats):
		league = stats["leagueName"]
		hotStreak = stats["hotStreak"]
		RankTier = str(stats["tier"]).title() + ' ' + str(stats["rank"])
		LP = str(stats["leaguePoints"]) + 'LP / '
		WinsLosses = str(stats["wins"]) + 'W' +  ' ' +  str(stats["losses"]) + 'L'
		WinRatio = 'Win Ratio ' + str(int(int(stats["wins"])/(int(stats["losses"]) + int(stats["wins"])) * 100)) + "%"
		final = Stats(league, RankTier, LP, WinsLosses, WinRatio, hotStreak)
		return final


	def get(self, request, **kwargs):
		#return render(request, 'app.html', context =None)
	#def post(self, request, **kwargs):
		APIKeyValue = APIKey()
		key = RiotWatcher(APIKeyValue)
		region = 'euw1'
		myProfileIconURLBase = '//opgg-static.akamaized.net/images/profile_icons/profileIcon[x].jpg'
		summonerNameSearch = self.request.GET.get('summonerName')
		soloTier = flexTier = ""
		soloStatsDisplay = flexStatsDisplay =""
		soloWinRate = []
		flexWinRate = []
		if Summoner.objects.filter(summoner_name = summonerNameSearch).count() > 0:
			print("Found")
			summoner = Summoner.objects.get(summoner_name = summonerNameSearch)
			mySummonerId = summoner.summonerID
			myAccountId = summoner.accountID
			myProfileIconId = summoner.profileIconId
			summonerNameSearch = summoner.summoner_name
			
			myProfileIconURL = myProfileIconURLBase.replace('[x]', str(myProfileIconId))
			print(str(mySummonerId) + ' ' + str(myProfileIconId))

#I could of also stored this data in a table in my database but I am not due to hand restraints
		else:
			
			try:
				summoner = key.summoner.by_name(region, summonerNameSearch)
				myProfileIconId = summoner["profileIconId"]
				myProfileIconURL = myProfileIconURLBase.replace('[x]', str(myProfileIconId))
				mySummonerId = summoner["id"]
				myAccountId = summoner["accountId"]
				summonerNameSearch = summoner["name"]

			except HTTPError as error:
				if error.response.status_code == 429:
				#Check documentation for explanations of error codes
					summoner = ('''An error has occured, due to too many requests have been made to the Riot API.  Please try again after '''.format(e.headers['Retry']) )
				elif error.response.status_code == 404:
					summoner = ('There is no summoner with that name on the region ' + region)
				return render(request, 'App.html', {
					'Summoner_Name' : summonerNameSearch,
					})

		matchHistory= key.match.matchlist_by_account(region, myAccountId, end_index = 5)['matches']
		games = []
		for x in matchHistory:
			print(x)
			games.append(Match(x, myAccountId, mySummonerId, summonerNameSearch, key))

		try:
			rankedStats= key.league.positions_by_summoner(region, mySummonerId)
			#print(rankedStats)
			flexStats = {}
			soloStats = {}
			for stats in rankedStats:
				if stats['queueType'] == "RANKED_SOLO_5x5":
					soloStats = stats
				elif stats['queueType'] == "RANKED_FLEX_SR":
					flexStats = stats



		except HTTPError as error:
			if error.response.status_code == 429:
			#Check documentation for explanations of error codes
				rankedStats = ('''An error has occured, due to too many requests have been made to the Riot API.  Please try again after '''.format(e.headers['Retry']) )
			elif error.response.status_code == 404:
				rankedStats = ('There is no summoner with that name on the region ' + region)
		if soloStats != {}:
			soloTier = soloStats["tier"]
			soloStatsDisplay = mySearch.displayStats(soloStats)
			soloWinRate = ChampWinRatios('solo', myAccountId, mySummonerId, summonerNameSearch, key)
		if flexStats != {}:
			flexTier = flexStats["tier"]
			flexStatsDisplay = mySearch.displayStats(flexStats)
			flexWinRate = ChampWinRatios('flex', myAccountId, mySummonerId, summonerNameSearch, key)
		highestTier = ""
		if flexStats == {} and soloStats == {}:
			return render(request, 'App.html',{'has_stats': False, 'Profile_Image' : myProfileIconURL, 'Summoner_Name': summonerNameSearch,})
		else:
			soloIndex = tiers.index(soloTier.lower())
			flexIndex = tiers.index(flexTier.lower())
			highestTier = tiers[max(soloIndex,flexIndex)]
			return render(request, 'App.html',{'has_stats': True,
				'Summoner_Name': summonerNameSearch,
				'Solo': soloStatsDisplay,
				'SoloChamps': soloWinRate[:5],
				'Profile_Image' : myProfileIconURL,
				'Flex': flexStatsDisplay,
				'FlexChamps': flexWinRate[:5],
				'highest_tier' : highestTier,
				'Queue_Type' : str(matchHistory),
				'matches': games,
			})

			
"""
class TestPageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'Test.html', context=None)
# Create your views here.
 """  
