from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
	
	name = models.CharField(max_length=100, unique=True)
	password = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	faction = models.CharField(max_length=100)
	town = models.CharField(max_length=100)
	world = models.IntegerField()
	coordinateX = models.IntegerField()
	coordinateY = models.IntegerField()
	lastlogin = models.IntegerField()

class Sawmill(models.Model):

	player = models.ForeignKey(Player, blank=False)
	level_build = models.IntegerField()
	capacity = models.IntegerField()
	quantity = models.IntegerField()
	material = models.CharField(max_length=100)
	production_hour = models.IntegerField()

class Barrack(models.Model):

	player = models.ForeignKey(Player, blank=False)
	level_build = models.IntegerField()

class Deposit(models.Model):

	player = models.ForeignKey(Player, blank=False)
	level_build = models.IntegerField()
	capacity = models.IntegerField()

class Army(models.Model):

	player = models.ForeignKey(Player, blank=False)
	unit1 = models.IntegerField()
	unit2 = models.IntegerField()
	unit3 = models.IntegerField()
	unit4 = models.IntegerField()
	unit5 = models.IntegerField()
	unit6 = models.IntegerField()
	unit7 = models.IntegerField()
	unit8 = models.IntegerField()
	unit9 = models.IntegerField()
	unit10 = models.IntegerField()
	unit99 = models.IntegerField()

class Farm(models.Model):

	player = models.ForeignKey(Player, blank=False)
	level_build = models.IntegerField()
	capacity = models.IntegerField()
	quantity = models.IntegerField()
	material = models.CharField(max_length=100)

class Intendency(models.Model):

	player = models.ForeignKey(Player, blank=False)
	level_build = models.IntegerField()

class Mine(models.Model):

	player = models.ForeignKey(Player, blank=False)
	level_build = models.IntegerField()
	capacity = models.IntegerField()
	quantity = models.IntegerField()
	material = models.CharField(max_length=100)
	production_hour = models.IntegerField()

class Wall(models.Model):

	player = models.ForeignKey(Player, blank=False)
	level_build = models.IntegerField()
	defence =  models.IntegerField()

class Event_update(models.Model):

	player = models.ForeignKey(Player, blank=False)
	time = models.IntegerField()
	procesed = models.IntegerField()
	build = models.CharField(max_length=100)

class Event_atack(models.Model):

	player = models.ForeignKey(Player, blank=False, related_name='player_atack')
	time = models.IntegerField()
	procesed = models.IntegerField()
	player_victim = models.ForeignKey(Player, blank=False, related_name='player_victim_atack')
	unit1 = models.IntegerField()
	unit2 = models.IntegerField()
	unit3 = models.IntegerField()
	unit4 = models.IntegerField()
	unit5 = models.IntegerField()
	unit6 = models.IntegerField()
	unit7 = models.IntegerField()
	unit8 = models.IntegerField()
	unit9 = models.IntegerField()
	unit10 = models.IntegerField()
	unit99 = models.IntegerField()
	back_time = models.IntegerField()
	wood = models.IntegerField()
	iron = models.IntegerField()

class Event_trade(models.Model):

	player = models.ForeignKey(Player, blank=False, related_name='player_trade')
	time = models.IntegerField()
	procesed = models.IntegerField()
	player_victim = models.ForeignKey(Player, blank=False, related_name='player_victim_trade')
	wood = models.IntegerField()
	iron = models.IntegerField()
	workers = models.IntegerField()
	back_time = models.IntegerField()

class Event_create(models.Model):

	player = models.ForeignKey(Player, blank=False)
	time = models.IntegerField()
	procesed = models.IntegerField()
	creature = models.IntegerField()
	quantity = models.IntegerField()

class Message(models.Model):

	transmitter = models.ForeignKey(Player, blank=False, related_name='player_transmitter')
	receiver = models.ForeignKey(Player, blank=False, related_name='player_receiver')
	title = models.CharField(max_length=100)
	text = models.TextField(max_length=500)
	read = models.IntegerField()
	date = models.DateField()
	time = models.IntegerField()

class Report_battle(models.Model):

	player = models.ForeignKey(Player, blank=False)
	text = models.TextField(max_length=500)
	date = models.CharField(max_length=100)
	time = models.IntegerField()
	victory = models.IntegerField()

class Report_trade(models.Model):

	player = models.ForeignKey(Player, blank=False)
	text = models.TextField(max_length=500)
	date = models.CharField(max_length=100)
	time = models.IntegerField()
	