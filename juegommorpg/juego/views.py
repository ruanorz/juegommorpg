# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, RequestContext
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect, Http404
from juego.models import Player, Sawmill, Barrack, Deposit, Army, Farm, Intendency, Mine, Wall, Event_update, Event_atack, Event_trade, Event_create, Message, Report_battle, Report_trade
import random
import time
import datetime
import math
from django.db.models import F




def index_view(request):

	mi_template = loader.get_template("index.html")

	return HttpResponse(mi_template.render())

def choose_faction(request):

	mi_template = loader.get_template("choose_faction.html")

	return render(request, "choose_faction.html")

def registration(request):

    if request.method == "POST":
    	
       	faccion = request.POST['faccion']
       	
       	return render(request, 'registration.html', {'faccion': faccion})

 
    return render(request, 'choose_faction.html')


def registrationComplete(request):

	if request.method == "POST":
		#obtenemos unas coordenadas libres en el mapa
		jugadores = Player.objects.all()
		numJugadores = len(jugadores)

		bandera=1
		contador=0
		while (int(bandera)==1):
			bandera=0
			coorX = int(random.randrange(6))
			coorY = int(random.randrange(6))
			for x in jugadores:
				if (int(x.coordinateX)==int(coorX)) and (int(x.coordinateY)==int(coorY)):
					bandera=1
		#En coorX y coorY y tenemos las posiciones libres
		#Ahora comprobamos que el usuario introducido no existe

		banderaNombre=0
		print banderaNombre
		for i in range(numJugadores):
			if jugadores[i].name==request.POST['nombre']:
			
				banderaNombre=1
				
		if request.POST['nombre']=="" or request.POST['password']=="" or request.POST['email']=="" or request.POST['aldea']=="":
			banderaNombre=1
		
		if banderaNombre==0:
			

			new_entry = Player(name=request.POST['nombre'], password=request.POST['password'], email=request.POST['email'], faction=request.POST['faccion'], town=request.POST['aldea'], world=1, coordinateX=coorX, coordinateY=coorY, lastlogin=time.time())
			new_entry.save()

			jugador = Player.objects.get(name=request.POST['nombre'])

			new_entry = Sawmill(level_build=1, capacity=1000, quantity=500, material='wood', production_hour=25, player_id=jugador.id)
			new_entry.save()

			new_entry = Barrack(level_build=1, player_id=jugador.id)
			new_entry.save()

			new_entry = Deposit(level_build=1, capacity=1000, player_id=jugador.id)
			new_entry.save()

			new_entry = Army(unit1=5, unit2=0, unit3=0, unit4=0, unit5=0, unit6=0, unit7=0, unit8=0, unit9=0, unit10=0, unit99=5, player_id=jugador.id)
			new_entry.save()

			new_entry = Farm(level_build=1, capacity=100, quantity=0, material='food', player_id=jugador.id)
			new_entry.save()

			new_entry = Intendency(level_build=1, player_id=jugador.id)
			new_entry.save()

			new_entry = Mine(level_build=1, capacity=1000, quantity=500, material='iron', production_hour=25, player_id=jugador.id)
			new_entry.save()

			new_entry = Wall(level_build=1, defence=20, player_id=jugador.id)
			new_entry.save()

			return render(request, 'registrationComplete.html')
       		
		else:
			#error en el registro, usuario repetido
			return render(request, 'registrationFail.html')



def login(request):

	return render(request, 'login.html')

def loginComplete(request):

	if request.method == "POST":
		request.POST['nombre']
		request.POST['password']

		try:
			jugadores = Player.objects.get(name=request.POST['nombre'], password=request.POST['password'])
		except Player.DoesNotExist:
			jugadores = None


		if jugadores != None:
			#login correcto
			#declaramos dos variables de sesion y redirigimos al juego
			request.session['player'] = jugadores.name
			request.session['faction'] = jugadores.faction
			request.session['playerID'] = jugadores.id

			return HttpResponseRedirect("/game/city/")

		else:
			#login incorrecto
			return HttpResponseRedirect("/accounts/login")

	else:
		#login incorrecto
		return HttpResponseRedirect("/accounts/login")


def city(request):

	if 'playerID' in request.session:
		#el usuario esta logueado correctamente

		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		return render(request, 'city.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4})
	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def world(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#Buscamos los jugadores del mundo
		jugadores = Player.objects.all()

		return render(request, 'world.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'jugadores': jugadores})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")

def playerAction(request, id):

	try:

		if 'playerID' in request.session:
			#--------------------------------------------
			nombreusuario=request.session['player']
			faccionusuario=request.session['faction']
			#cargamos los recursos del usuario
			jugador = Player.objects.get(name=request.session['player'])
			ultima_conexion=jugador.lastlogin
			nombrepoblado=jugador.town.upper()

			aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
			produccion_hora_madera = aserradero.production_hour
			cantidad_madera = aserradero.quantity
			cap_madera = aserradero.capacity

			mina = Mine.objects.get(player_id=request.session['playerID'])
			produccion_hora_metal = mina.production_hour
			cantidad_metal = mina.quantity
			cap_metal = mina.capacity

			granja = Farm.objects.get(player_id=request.session['playerID'])
			cantidad = granja.quantity
			capacidad = granja.capacity

			#calculamos la cantidad actual que tiene
			madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
			metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

			ratiosumamadera=float(produccion_hora_madera)/3600
			ratiosumametal=float(produccion_hora_metal)/3600

			#Cargamos las unidades que tiene el jugador
			ejercito = Army.objects.get(player_id=request.session['playerID'])
			unidad1=ejercito.unit1
			unidad2=ejercito.unit2
			unidad3=ejercito.unit3
			unidad4=ejercito.unit4
			unidad5=ejercito.unit5
			unidad6=ejercito.unit6
			unidad7=ejercito.unit7
			unidad8=ejercito.unit8
			unidad9=ejercito.unit9
			unidad10=ejercito.unit10
			unidad99=ejercito.unit99

			#leemos el fichero ejercito.txt para obtener el nombre de las unidades
			#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
			#lines = txtejercito.readlines()

			#lines[0].split(':')
			tiempotope=time.time();
			tiempotope2=time.time();
			tiempotope3=time.time();
			tiempotope4=time.time();
			edificioactualizado=0
			cantidad2=0
			vuelta3=0
			vuelta4=0
			#Miramos los contadores de los eventos
			try:
				eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_update.DoesNotExist:
				eventoactualiza = None
			if eventoactualiza != None:
				for x in eventoactualiza:
					tiempotope = eventoactualiza[0].time
					edificioactualizado = eventoactualiza[0].build

			try:
				eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_create.DoesNotExist:
				eventocrea = None
			if eventocrea != None:
				for x in eventocrea:
					tiempotope2 = x.time
					cantidad2 = x.quantity

			try:
				eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_atack.DoesNotExist:
				eventoataca = None
			if eventoataca != None:
				for x in eventoataca:
					tiempotope3 = x.time
					vuelta3 = x.back_time

			try:
				eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_trade.DoesNotExist:
				eventocomercia = None
			if eventocomercia != None:
				for x in eventocomercia:
					tiempotope4 = x.time
					vuelta4 = x.back_time


			#calculamos tiempos
			tiempoactual=time.time();
			
			
			restante=tiempotope-tiempoactual;
			restante2=tiempotope2-tiempoactual;
			restante3=tiempotope3-tiempoactual;
			restante4=tiempotope4-tiempoactual;
				
			#------------------------------


			idtio=int(id)

			#PREGUNTAMOS POR LA FACCION DE ESE TIO
			tio = Player.objects.get(id=idtio)
			facciontio = tio.faction
			#faccionusuario


			return render(request, 'playerAction.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'facciontio': facciontio, 'tio': tio, 'jugador': jugador})

		else:
			#El usuario no esta logueado
			return HttpResponseRedirect("/accounts/login")

	except Player.DoesNotExist:
		raise Http404

def intendency(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;
		
		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		#CONSULTA PARA SACAR EL NIVEL DE LA INTENDENCIA
		intendencia = Intendency.objects.get(player_id=request.session['playerID'])
		nivel = intendencia.level_build

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtintendencia = open('juego/static/ficheros/intendencianiveles.txt', 'r')
		lines = txtintendencia.readlines()

		linea = lines[nivel].split(':')
		
		costemadera = int(linea[2])
		costemetal = int(linea[3])
		

		return render(request, 'intendency.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")
	

def intendencyUpgrade(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;

		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		#CONSULTA PARA SACAR EL NIVEL DE LA INTENDENCIA
		intendencia = Intendency.objects.get(player_id=request.session['playerID'])
		nivel = intendencia.level_build

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtintendencia = open('juego/static/ficheros/intendencianiveles.txt', 'r')
		lines = txtintendencia.readlines()

		linea = lines[nivel].split(':')
		
		costemadera = int(linea[2])
		costemetal = int(linea[3])
		tiempo = time.time()+int(linea[4])

		#AGREGAMOS EN LA TABLA DE LAS ACTUALIZACIONES UNA ENTRADA
		new_entry = Event_update(time=tiempo, procesed=0, build='intendencia', player_id=jugador.id)
		new_entry.save()

		#SI LA MADERA QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE LA MADERA AL CAP
		if ((((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))>int(cap_madera)):
			kk=int(cap_madera)-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE A LA MADERA TOTAL
			madera=(((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=madera)
			#new_entry.save()
		#SI EL METAL QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE EL METAL AL CAP
		if ((((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+int(cantidad_metal))>int(cap_metal)):
			kk=int(cap_metal)-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE AL METAL TOTAL
			metal=(((time.time()-int(ultima_conexion))*(float(produccion_hora_metal)/3600))+int(cantidad_metal))-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=metal)
			#new_entry.save()


		timeactualizado=time.time();
		
		#COMO HEMOS ACTUALIZADO LA CANTIDAD DE MADERA Y METAL, ACTUALIZAMOS EL CAMPO DE ULTIMA CONEXION
		new_entry = Player.objects.filter(id=request.session['playerID']).update(lastlogin=timeactualizado)
		#new_entry.save()

		return render(request, 'intendencyUpgrade.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def intendencyWorkers(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------


		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		#CONSULTA PARA SACAR EL NIVEL DE LA INTENDENCIA
		intendencia = Intendency.objects.get(player_id=request.session['playerID'])
		nivel = intendencia.level_build

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtintendencia = open('juego/static/ficheros/aldeanos.txt', 'r')
		lines = txtintendencia.readlines()

		valores = lines[0].split(':')
		

		
		kk=capacidad-cantidad;
		max1=math.floor(madera/int(valores[7]));
		max2=math.floor(metal/int(valores[8]));
		max3=math.floor(kk/int(valores[9]));
		
		maxi=1000;
		if (max1<maxi):
			maxi=max1
		
		if (max2<maxi):
			maxi=max2
		
		if(max3<maxi):
			maxi=max3



		return render(request, 'intendencyWorkers.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'nivel': nivel, 'maxi': int(maxi)})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")

def intendencyWorkersComplete(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		cant=request.POST['rangeInput'];



		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		#CONSULTA PARA SACAR EL NIVEL DE LA INTENDENCIA
		intendencia = Intendency.objects.get(player_id=request.session['playerID'])
		nivel = intendencia.level_build

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtintendencia = open('juego/static/ficheros/aldeanos.txt', 'r')
		lines = txtintendencia.readlines()

		valores = lines[0].split(':')
		
		costemadera=int(valores[7])*int(cant);
		costemetal=int(valores[8])*int(cant);
		costecomida=int(valores[9])*int(cant);
		
		comidatotal=int(cantidad)+int(costecomida);

		timeactualizado=time.time();
		tiempo=timeactualizado+(int(valores[12])*int(cant));
		
		
		#SI LA MADERA QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE LA MADERA AL CAP
		if ((((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))>int(cap_madera)):
			kk=int(cap_madera)-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE A LA MADERA TOTAL
			madera=(((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=madera)
			#new_entry.save()
		#SI EL METAL QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE EL METAL AL CAP
		if ((((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+int(cantidad_metal))>int(cap_metal)):
			kk=int(cap_metal)-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE AL METAL TOTAL
			metal=(((time.time()-int(ultima_conexion))*(float(produccion_hora_metal)/3600))+int(cantidad_metal))-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=metal)
			#new_entry.save()


		#AUMENTAMOS TAMBIEN LA COMIDA
		new_entry = Farm.objects.filter(player_id=request.session['playerID']).update(quantity=comidatotal)


		timeactualizado=time.time();
		
		#COMO HEMOS ACTUALIZADO LA CANTIDAD DE MADERA Y METAL, ACTUALIZAMOS EL CAMPO DE ULTIMA CONEXION
		new_entry = Player.objects.filter(id=request.session['playerID']).update(lastlogin=timeactualizado)
		#new_entry.save()


		#POR ULTIMO AGREGAMOS UNA NUEVA ENTRADA A LA TABLA DE CREACIONES
		new_entry = Event_create(time=tiempo, player_id=jugador.id, procesed=0, creature=99, quantity=cant)
		new_entry.save()


		return render(request, 'intendencyWorkersComplete.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'nivel': nivel})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def sawmill(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;
		
		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity
		nivel = aserradero.level_build
		
		

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtintendencia = open('juego/static/ficheros/aserraderoniveles.txt', 'r')
		lines = txtintendencia.readlines()

		linea = lines[nivel].split(':')
		
		costemadera = int(linea[2])
		costemetal = int(linea[3])
		

		return render(request, 'sawmill.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso, 'cap_madera': cap_madera, 'produccion_hora_madera': produccion_hora_madera})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def sawmillUpgrade(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;

		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity
		nivel = aserradero.level_build
		
		

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtaserradero = open('juego/static/ficheros/aserraderoniveles.txt', 'r')
		lines = txtaserradero.readlines()

		valores = lines[nivel].split(':')
		
		costemadera = int(valores[2])
		costemetal = int(valores[3])
		tiempo = time.time()+int(valores[4])

		#AGREGAMOS EN LA TABLA DE LAS ACTUALIZACIONES UNA ENTRADA
		new_entry = Event_update(time=tiempo, procesed=0, build='aserradero', player_id=jugador.id)
		new_entry.save()

		#SI LA MADERA QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE LA MADERA AL CAP
		if ((((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))>int(cap_madera)):
			kk=int(cap_madera)-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE A LA MADERA TOTAL
			madera=(((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=madera)
			#new_entry.save()
			#SI EL METAL QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE EL METAL AL CAP
		if ((((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+int(cantidad_metal))>int(cap_metal)):
			kk=int(cap_metal)-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE AL METAL TOTAL
			metal=(((time.time()-int(ultima_conexion))*(float(produccion_hora_metal)/3600))+int(cantidad_metal))-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=metal)
			#new_entry.save()


		timeactualizado=time.time();
		
		#COMO HEMOS ACTUALIZADO LA CANTIDAD DE MADERA Y METAL, ACTUALIZAMOS EL CAMPO DE ULTIMA CONEXION
		new_entry = Player.objects.filter(id=request.session['playerID']).update(lastlogin=timeactualizado)
		#new_entry.save()

		return render(request, 'sawmillUpgrade.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def mines(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;
		
		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity
		nivel = mina.level_build

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity
			
		

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtmina = open('juego/static/ficheros/minaniveles.txt', 'r')
		lines = txtmina.readlines()

		linea = lines[nivel].split(':')
		
		costemadera = int(linea[2])
		costemetal = int(linea[3])
		

		return render(request, 'mine.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso, 'cap_madera': cap_madera, 'produccion_hora_madera': produccion_hora_madera})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def minesUpgrade(request):
	
	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;

		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity
		nivel = mina.level_build

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity
		
				

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtaserradero = open('juego/static/ficheros/aserraderoniveles.txt', 'r')
		lines = txtaserradero.readlines()

		valores = lines[nivel].split(':')
		
		costemadera = int(valores[2])
		costemetal = int(valores[3])
		tiempo = time.time()+int(valores[4])

		#AGREGAMOS EN LA TABLA DE LAS ACTUALIZACIONES UNA ENTRADA
		new_entry = Event_update(time=tiempo, procesed=0, build='mina', player_id=jugador.id)
		new_entry.save()

		#SI LA MADERA QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE LA MADERA AL CAP
		if ((((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))>int(cap_madera)):
			kk=int(cap_madera)-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE A LA MADERA TOTAL
			madera=(((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=madera)
			#new_entry.save()
		#SI EL METAL QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE EL METAL AL CAP
		if ((((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+int(cantidad_metal))>int(cap_metal)):
			kk=int(cap_metal)-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE AL METAL TOTAL
			metal=(((time.time()-int(ultima_conexion))*(float(produccion_hora_metal)/3600))+int(cantidad_metal))-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=metal)
			#new_entry.save()


		timeactualizado=time.time();
		
		#COMO HEMOS ACTUALIZADO LA CANTIDAD DE MADERA Y METAL, ACTUALIZAMOS EL CAMPO DE ULTIMA CONEXION
		new_entry = Player.objects.filter(id=request.session['playerID']).update(lastlogin=timeactualizado)
		#new_entry.save()

		return render(request, 'mineUpgrade.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def farm(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;
		
		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity


		#CONSULTA PARA SACAR EL NIVEL DE LA GRANJA
		granja = Farm.objects.get(player_id=request.session['playerID'])
		nivel = granja.level_build
			
		

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtmina = open('juego/static/ficheros/granjaniveles.txt', 'r')
		lines = txtmina.readlines()

		linea = lines[nivel].split(':')
		
		costemadera = int(linea[2])
		costemetal = int(linea[3])
		

		return render(request, 'farm.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso, 'cap_madera': cap_madera, 'produccion_hora_madera': produccion_hora_madera})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def farmUpgrade(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;

		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity
		

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity
		
		#CONSULTA PARA SACAR EL NIVEL DE LA GRANJA
		granja = Farm.objects.get(player_id=request.session['playerID'])
		nivel = granja.level_build

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtaserradero = open('juego/static/ficheros/granjaniveles.txt', 'r')
		lines = txtaserradero.readlines()

		valores = lines[nivel].split(':')
		
		costemadera = int(valores[2])
		costemetal = int(valores[3])
		tiempo = time.time()+int(valores[4])

		#AGREGAMOS EN LA TABLA DE LAS ACTUALIZACIONES UNA ENTRADA
		new_entry = Event_update(time=tiempo, procesed=0, build='granja', player_id=jugador.id)
		new_entry.save()

		#SI LA MADERA QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE LA MADERA AL CAP
		if ((((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))>int(cap_madera)):
			kk=int(cap_madera)-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE A LA MADERA TOTAL
			madera=(((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=madera)
			#new_entry.save()
		#SI EL METAL QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE EL METAL AL CAP
		if ((((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+int(cantidad_metal))>int(cap_metal)):
			kk=int(cap_metal)-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE AL METAL TOTAL
			metal=(((time.time()-int(ultima_conexion))*(float(produccion_hora_metal)/3600))+int(cantidad_metal))-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=metal)
			#new_entry.save()


		timeactualizado=time.time();
		
		#COMO HEMOS ACTUALIZADO LA CANTIDAD DE MADERA Y METAL, ACTUALIZAMOS EL CAMPO DE ULTIMA CONEXION
		new_entry = Player.objects.filter(id=request.session['playerID']).update(lastlogin=timeactualizado)
		#new_entry.save()

		return render(request, 'farmUpgrade.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def deposit(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;
		
		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity


		#CONSULTA PARA SACAR EL NIVEL DEL DEPOSITO
		deposito = Deposit.objects.get(player_id=request.session['playerID'])
		nivel = deposito.level_build
			
		

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtmina = open('juego/static/ficheros/depositoniveles.txt', 'r')
		lines = txtmina.readlines()

		linea = lines[nivel].split(':')
		
		costemadera = int(linea[2])
		costemetal = int(linea[3])
		

		return render(request, 'deposit.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso, 'cap_madera': cap_madera, 'produccion_hora_madera': produccion_hora_madera})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")

def depositUpgrade(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;

		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity
		

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity
		
		#CONSULTA PARA SACAR EL NIVEL DE LA GRANJA
		granja = Farm.objects.get(player_id=request.session['playerID'])
		nivel = granja.level_build

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtaserradero = open('juego/static/ficheros/depositoniveles.txt', 'r')
		lines = txtaserradero.readlines()

		valores = lines[nivel].split(':')
		
		costemadera = int(valores[2])
		costemetal = int(valores[3])
		tiempo = time.time()+int(valores[4])

		#AGREGAMOS EN LA TABLA DE LAS ACTUALIZACIONES UNA ENTRADA
		new_entry = Event_update(time=tiempo, procesed=0, build='deposito', player_id=jugador.id)
		new_entry.save()

		#SI LA MADERA QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE LA MADERA AL CAP
		if ((((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))>int(cap_madera)):
			kk=int(cap_madera)-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE A LA MADERA TOTAL
			madera=(((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=madera)
			#new_entry.save()
		#SI EL METAL QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE EL METAL AL CAP
		if ((((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+int(cantidad_metal))>int(cap_metal)):
			kk=int(cap_metal)-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE AL METAL TOTAL
			metal=(((time.time()-int(ultima_conexion))*(float(produccion_hora_metal)/3600))+int(cantidad_metal))-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=metal)
			#new_entry.save()


		timeactualizado=time.time();
		
		#COMO HEMOS ACTUALIZADO LA CANTIDAD DE MADERA Y METAL, ACTUALIZAMOS EL CAMPO DE ULTIMA CONEXION
		new_entry = Player.objects.filter(id=request.session['playerID']).update(lastlogin=timeactualizado)
		#new_entry.save()

		return render(request, 'depositUpgrade.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")

def wall(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;
		
		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity


		#CONSULTA PARA SACAR EL NIVEL DE LA MURALLA
		muralla = Wall.objects.get(player_id=request.session['playerID'])
		nivel = muralla.level_build
		defensa = muralla.defence
			
		

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtmina = open('juego/static/ficheros/depositoniveles.txt', 'r')
		lines = txtmina.readlines()

		linea = lines[nivel].split(':')
		
		costemadera = int(linea[2])
		costemetal = int(linea[3])
		

		return render(request, 'wall.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso, 'cap_madera': cap_madera, 'produccion_hora_madera': produccion_hora_madera, 'defensa': defensa})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")

def wallUpgrade(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;

		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity
		

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity
		
		#CONSULTA PARA SACAR EL NIVEL DE LA MURALLA
		muralla = Wall.objects.get(player_id=request.session['playerID'])
		nivel = muralla.level_build

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtaserradero = open('juego/static/ficheros/murallaniveles.txt', 'r')
		lines = txtaserradero.readlines()

		valores = lines[nivel].split(':')
		
		costemadera = int(valores[2])
		costemetal = int(valores[3])
		tiempo = time.time()+int(valores[4])

		#AGREGAMOS EN LA TABLA DE LAS ACTUALIZACIONES UNA ENTRADA
		new_entry = Event_update(time=tiempo, procesed=0, build='muralla', player_id=jugador.id)
		new_entry.save()

		#SI LA MADERA QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE LA MADERA AL CAP
		if ((((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))>int(cap_madera)):
			kk=int(cap_madera)-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE A LA MADERA TOTAL
			madera=(((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=madera)
			#new_entry.save()
		#SI EL METAL QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE EL METAL AL CAP
		if ((((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+int(cantidad_metal))>int(cap_metal)):
			kk=int(cap_metal)-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE AL METAL TOTAL
			metal=(((time.time()-int(ultima_conexion))*(float(produccion_hora_metal)/3600))+int(cantidad_metal))-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=metal)
			#new_entry.save()


		timeactualizado=time.time();
		
		#COMO HEMOS ACTUALIZADO LA CANTIDAD DE MADERA Y METAL, ACTUALIZAMOS EL CAMPO DE ULTIMA CONEXION
		new_entry = Player.objects.filter(id=request.session['playerID']).update(lastlogin=timeactualizado)
		#new_entry.save()

		return render(request, 'wallUpgrade.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def barrack(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;
		
		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		#CONSULTA PARA SACAR EL NIVEL DE LA INTENDENCIA
		cuartel = Barrack.objects.get(player_id=request.session['playerID'])
		nivel = cuartel.level_build

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtintendencia = open('juego/static/ficheros/cuartelniveles.txt', 'r')
		lines = txtintendencia.readlines()

		linea = lines[nivel].split(':')
		
		costemadera = int(linea[2])
		costemetal = int(linea[3])
		

		return render(request, 'barrack.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def barrackUpgrade(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		#CONSULTA PARA VER SI HAY YA UN EDIFICIO ACTUALIZANDOSE
		actualizacionencurso=0;
		try:
			eventoactualiza2 = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza2 = None
		if eventoactualiza2 != None:
			for x in eventoactualiza2:
				actualizacionencurso=1;

		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		#CONSULTA PARA SACAR EL NIVEL DE LA INTENDENCIA
		cuartel = Barrack.objects.get(player_id=request.session['playerID'])
		nivel = cuartel.level_build

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtintendencia = open('juego/static/ficheros/cuartelniveles.txt', 'r')
		lines = txtintendencia.readlines()

		linea = lines[nivel].split(':')
		
		costemadera = int(linea[2])
		costemetal = int(linea[3])
		tiempo = time.time()+int(linea[4])

		#AGREGAMOS EN LA TABLA DE LAS ACTUALIZACIONES UNA ENTRADA
		new_entry = Event_update(time=tiempo, procesed=0, build='cuartel', player_id=jugador.id)
		new_entry.save()

		#SI LA MADERA QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE LA MADERA AL CAP
		if ((((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))>int(cap_madera)):
			kk=int(cap_madera)-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE A LA MADERA TOTAL
			madera=(((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=madera)
			#new_entry.save()
		#SI EL METAL QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE EL METAL AL CAP
		if ((((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+int(cantidad_metal))>int(cap_metal)):
			kk=int(cap_metal)-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE AL METAL TOTAL
			metal=(((time.time()-int(ultima_conexion))*(float(produccion_hora_metal)/3600))+int(cantidad_metal))-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=metal)
			#new_entry.save()
		

		timeactualizado=time.time();
		
		#COMO HEMOS ACTUALIZADO LA CANTIDAD DE MADERA Y METAL, ACTUALIZAMOS EL CAMPO DE ULTIMA CONEXION
		new_entry = Player.objects.filter(id=request.session['playerID']).update(lastlogin=timeactualizado)
		#new_entry.save()

		return render(request, 'barrackUpgrade.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'costemadera': costemadera, 'costemetal': costemetal, 'nivel': nivel, 'actualizacionencurso': actualizacionencurso})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def barrackArmy(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------
		#CONSULTAMOS EL NIVEL DEL CUARTEL
		cuartel = Barrack.objects.get(player_id=request.session['playerID'])
		nivel = cuartel.level_build

		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		#CONSULTA PARA SACAR EL NIVEL DE LA INTENDENCIA
		intendencia = Intendency.objects.get(player_id=request.session['playerID'])
		nivel = intendencia.level_build

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtintendencia = open('juego/static/ficheros/ejercito.txt', 'r')
		lines = txtintendencia.readlines()

		y=0
		buenos=[]
		for x in range(10):
			separados = lines[x].split(':')
			if int(separados[10]) <= nivel:
				buenos.append(separados)
				y=y+1
		


		return render(request, 'barrackArmy.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'nivel': nivel, 'buenos': buenos})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def barrackArmy2(request, id):


	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		lines = txtejercito.readlines()

		if int(id) > 10:
			raise Http404

		valores = lines[int(id)-1].split(':')

		idbicho=int(id)

		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

	

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		
		

		
		kk=capacidad-cantidad;
		max1=math.floor(madera/int(valores[7]));
		max2=math.floor(metal/int(valores[8]));
		max3=math.floor(kk/int(valores[9]));
		
		maxi=1000;
		if (max1<maxi):
			maxi=max1
		
		if (max2<maxi):
			maxi=max2
		
		if(max3<maxi):
			maxi=max3



		return render(request, 'barrackArmy2.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'maxi': int(maxi), 'valores': valores, 'idbicho': idbicho})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def barrackArmy2Complete(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time



		
		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		cant=request.POST['rangeInput'];
		idbicho=request.POST['idbicho'];


		#CONSULTA PARA SACAR LA ULTIMA HORA DE CONEXION PARA DESPUES CALCULAR LOS RECURSOS QUE TIENE
		jugador2 = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador2.lastlogin

		#CONSULTA PARA SACAR EL METAL QUE TIENE ACTUALMENTE
		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		#CONSULTA PARA SACAR LA MADERA QUE TIENE ACTUALMENTE
		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		#CONSULTA PARA SACAR EL NIVEL DE LA INTENDENCIA
		intendencia = Intendency.objects.get(player_id=request.session['playerID'])
		nivel = intendencia.level_build

		#CALCULAMOS LA MADERA QUE TIENE EN ESTE MOMENTO CON LOS DATOS OBTENIDOS
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera;
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal;

		#SACAMOS DEL FICHERO LO QUE CUESTA SUBIR DE NIVEL EL EDIFICIO
		txtintendencia = open('juego/static/ficheros/ejercito.txt', 'r')
		lines = txtintendencia.readlines()

		valores = lines[int(idbicho)-1].split(':')
		
		costemadera=int(valores[7])*int(cant);
		costemetal=int(valores[8])*int(cant);
		costecomida=int(valores[9])*int(cant);
		
		comidatotal=int(cantidad)+int(costecomida);

		timeactualizado=time.time();
		tiempo=timeactualizado+(int(valores[12])*int(cant));
		
		
		#SI LA MADERA QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE LA MADERA AL CAP
		if ((((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))>int(cap_madera)):
			kk=int(cap_madera)-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
		#SINO, QUITA EL COSTE A LA MADERA TOTAL
			madera=(((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))-int(costemadera);
			new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=madera)
			#new_entry.save()
		#SI EL METAL QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE EL METAL AL CAP
		if ((((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+int(cantidad_metal))>int(cap_metal)):
			kk=int(cap_metal)-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
			#new_entry.save()
		else:
			#SINO, QUITA EL COSTE AL METAL TOTAL
			metal=(((time.time()-int(ultima_conexion))*(float(produccion_hora_metal)/3600))+int(cantidad_metal))-int(costemetal);
			new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=metal)
			#new_entry.save()


		#AUMENTAMOS TAMBIEN LA COMIDA
		new_entry = Farm.objects.filter(player_id=request.session['playerID']).update(quantity=comidatotal)


		timeactualizado=time.time();
		
		#COMO HEMOS ACTUALIZADO LA CANTIDAD DE MADERA Y METAL, ACTUALIZAMOS EL CAMPO DE ULTIMA CONEXION
		new_entry = Player.objects.filter(id=request.session['playerID']).update(lastlogin=timeactualizado)
		#new_entry.save()


		#POR ULTIMO AGREGAMOS UNA NUEVA ENTRADA A LA TABLA DE CREACIONES
		new_entry = Event_create(time=tiempo, player_id=jugador.id, procesed=0, creature=idbicho, quantity=cant)
		new_entry.save()


		return render(request, 'barrackArmy2Complete.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'nivel': nivel})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def attack(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------


		user = request.POST['idtio']

		#PREGUNTAMOS POR LA FACCION DE ESE TIO
		tio = Player.objects.get(id=user)
		facciontio = tio.faction
		#faccionusuario

		txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		lines = txtejercito.readlines()

		valores0 = lines[0].split(':')
		valores1 = lines[1].split(':')
		valores2 = lines[2].split(':')
		valores3 = lines[3].split(':')
		valores4 = lines[4].split(':')
		valores5 = lines[5].split(':')
		valores6 = lines[6].split(':')
		valores7 = lines[7].split(':')
		valores8 = lines[8].split(':')
		valores9 = lines[9].split(':')

		txtaldeanos = open('juego/static/ficheros/aldeanos.txt', 'r')
		lines = txtaldeanos.readlines()

		valores99 = lines[0].split(':')

		return render(request, 'attack.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'facciontio': facciontio, 'tio': tio, 'jugador': jugador, 'valores0': valores0, 'valores1': valores1, 'valores2': valores2, 'valores3': valores3, 'valores4': valores4, 'valores5': valores5, 'valores6': valores6, 'valores7': valores7, 'valores8': valores8, 'valores9': valores9, 'valores99': valores99})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")



def attackComplete(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()
		pruebax=jugador.coordinateX
		pruebay=jugador.coordinateY
		id_usuario=jugador.id

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------


		user = request.POST['idtio']

		unidad1a=0
		unidad2a=0
		unidad3a=0
		unidad4a=0
		unidad5a=0
		unidad6a=0
		unidad7a=0
		unidad8a=0
		unidad9a=0
		unidad10a=0
		unidad99a=0

		unidad1a=int(request.POST['rangeInput'])
		unidad2a=int(request.POST['rangeInput2'])
		unidad3a=int(request.POST['rangeInput3'])
		unidad4a=int(request.POST['rangeInput4'])
		unidad5a=int(request.POST['rangeInput5'])
		unidad6a=int(request.POST['rangeInput6'])
		unidad7a=int(request.POST['rangeInput7'])
		unidad8a=int(request.POST['rangeInput8'])
		unidad9a=int(request.POST['rangeInput9'])
		unidad10a=int(request.POST['rangeInput10'])
		unidad99a=int(request.POST['rangeInput11'])

		vel1 = 0
		vel2 = 0
		vel3 = 0
		vel4 = 0
		vel5 = 0
		vel6 = 0
		vel7 = 0
		vel8 = 0
		vel9 = 0
		vel10 = 0
		vel11 = 0


		if unidad1a != 0 or unidad2a != 0 or unidad3a != 0 or unidad4a != 0 or unidad5a != 0 or unidad6a != 0 or unidad7a != 0 or unidad8a != 0 or unidad9a != 0 or unidad10a != 0 or unidad99a != 0 :
			
			txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
			lines = txtejercito.readlines()

			if unidad1a != 0:
				valores = lines[0].split(':')
				vel1=valores[6]

			if unidad2a != 0:
				valores = lines[1].split(':')
				vel2=valores[6]

			if unidad3a != 0:
				valores = lines[2].split(':')
				vel3=valores[6]

			if unidad4a != 0:
				valores = lines[3].split(':')
				vel4=valores[6]

			if unidad5a != 0:
				valores = lines[4].split(':')
				vel5=valores[6]

			if unidad6a != 0:
				valores = lines[5].split(':')
				vel6=valores[6]

			if unidad7a != 0:
				valores = lines[6].split(':')
				vel7=valores[6]

			if unidad8a != 0:
				valores = lines[7].split(':')
				vel8=valores[6]

			if unidad9a != 0:
				valores = lines[8].split(':')
				vel9=valores[6]

			if unidad10a != 0:
				valores = lines[9].split(':')
				vel10=valores[6]

			txtaldeanos = open('juego/static/ficheros/aldeanos.txt', 'r')
			lines = txtaldeanos.readlines()

			if unidad99a != 0:
				valores = lines[0].split(':')
				vel11=valores[6]

			velocidad=10.0

			if (float(vel1) < float(velocidad)) and (float(vel1) != 0):
				velocidad = float(vel1)

			if (float(vel2) < float(velocidad)) and (float(vel2) != 0):
				velocidad = float(vel2)

			if (float(vel3) < float(velocidad)) and (float(vel3) != 0):
				velocidad = float(vel3)

			if (float(vel4) < float(velocidad)) and (float(vel4) != 0):
				velocidad = float(vel4)

			if (float(vel5) < float(velocidad)) and (float(vel5) != 0):
				velocidad = float(vel5)

			if (float(vel6) < float(velocidad)) and (float(vel6) != 0):
				velocidad = float(vel6)

			if (float(vel7) < float(velocidad)) and (float(vel7) != 0):
				velocidad = float(vel7)

			if (float(vel8) < float(velocidad)) and (float(vel8) != 0):
				velocidad = float(vel8)

			if (float(vel9) < float(velocidad)) and (float(vel9) != 0):
				velocidad = float(vel9)

			if (float(vel10) < float(velocidad)) and (float(vel10) != 0):
				velocidad = float(vel10)

			if (float(vel11) < float(velocidad)) and (float(vel11) != 0):
				velocidad = float(vel11)

			#CONSULTA SACA LAS COORDENADAS DEL USUARIO ELEGIDO
			tio = Player.objects.get(id=user)
			coordenadaxuser = tio.coordinateX
			coordenadayuser = tio.coordinateY
			#pruebax
			#pruebay

			#CALCULAMOS LA DISTANCIA DE UNA ALDEA A OTRA
			
			distancia=pow(((pow((int(coordenadaxuser)-int(pruebax)),2))+(pow((int(coordenadayuser)-int(pruebay)),2))),0.5)
			tiempototal=int(distancia)*600
			tiempototaldoble=int(tiempototal)*2
			
			tiempo0=time.time()+int(tiempototal)
			tiempo1=time.time()+int(tiempototaldoble)

			#INSERTAMOS UN REGISTRO EN EVENTOATACAR POR ULTIMO
			#IDA
			new_entry = Event_atack(player_id=jugador.id, time=tiempo0, procesed=0, player_victim_id=tio.id, unit1=unidad1a, unit2=unidad2a, unit3=unidad3a, unit4=unidad4a, unit5=unidad5a, unit6=unidad6a, unit7=unidad7a, unit8=unidad8a, unit9=unidad9a, unit10=unidad10a, unit99=unidad99a, back_time=0, wood=0, iron=0)
			new_entry.save()
			
			#VUELTA
			new_entry = Event_atack(player_id=jugador.id, time=tiempo1, procesed=0, player_victim_id=tio.id, unit1=unidad1a, unit2=unidad2a, unit3=unidad3a, unit4=unidad4a, unit5=unidad5a, unit6=unidad6a, unit7=unidad7a, unit8=unidad8a, unit9=unidad9a, unit10=unidad10a, unit99=unidad99a, back_time=1, wood=0, iron=0)
			new_entry.save()
			
			
			#SACAMOS DE LA TABLA EJERCITO LAS UNIDADES UTILIZADAS
			new_entry = Army.objects.filter(player_id=request.session['playerID']).update(unit1=F('unit1') - unidad1a)
			new_entry = Army.objects.filter(player_id=request.session['playerID']).update(unit2=F('unit2') - unidad2a)
			new_entry = Army.objects.filter(player_id=request.session['playerID']).update(unit3=F('unit3') - unidad3a)
			new_entry = Army.objects.filter(player_id=request.session['playerID']).update(unit4=F('unit4') - unidad4a)
			new_entry = Army.objects.filter(player_id=request.session['playerID']).update(unit5=F('unit5') - unidad5a)
			new_entry = Army.objects.filter(player_id=request.session['playerID']).update(unit6=F('unit6') - unidad6a)
			new_entry = Army.objects.filter(player_id=request.session['playerID']).update(unit7=F('unit7') - unidad7a)
			new_entry = Army.objects.filter(player_id=request.session['playerID']).update(unit8=F('unit8') - unidad8a)
			new_entry = Army.objects.filter(player_id=request.session['playerID']).update(unit9=F('unit9') - unidad9a)
			new_entry = Army.objects.filter(player_id=request.session['playerID']).update(unit10=F('unit10') - unidad10a)
			new_entry = Army.objects.filter(player_id=request.session['playerID']).update(unit99=F('unit99') - unidad99a)

			return render(request, 'attackComplete.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'tio': tio, 'jugador': jugador})

		else:
			return HttpResponseRedirect("/game/world")
	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def trade(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------


		user = request.POST['idtio']

		#PREGUNTAMOS POR LA FACCION DE ESE TIO
		tio = Player.objects.get(id=user)
		facciontio = tio.faction
		#faccionusuario
		maxi = unidad99

		txtaldeanos = open('juego/static/ficheros/aldeanos.txt', 'r')
		lines = txtaldeanos.readlines()

		valores = lines[0].split(':')

		return render(request, 'trade.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'facciontio': facciontio, 'tio': tio, 'jugador': jugador, 'valores': valores, 'maxi': maxi})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def trade2(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------


		user = request.POST['idtio']
		numero_aldeanos=request.POST['rangeInput'];

		#PREGUNTAMOS POR LA FACCION DE ESE TIO
		tio = Player.objects.get(id=user)
		

		#CONSULTA PARA SACAR EL NIVEL DE LA INTENDENCIA
		intendencia = Intendency.objects.get(player_id=request.session['playerID'])
		nivel = intendencia.level_build


		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		#CALCULAMOS LOS MATS QUE PUEDEN TRANSPORTAR LOS ALDEANOS ELEGIDOS
		cantidad_materiales_tranportan_aldeanos=int(nivel)*int(numero_aldeanos)*5;
		

		if cantidad_materiales_tranportan_aldeanos > madera:
			max_madera = madera
		else:
			max_madera = cantidad_materiales_tranportan_aldeanos	
		
		if cantidad_materiales_tranportan_aldeanos > metal:
			max_metal = metal
		else:
			max_metal = cantidad_materiales_tranportan_aldeanos	
		

		return render(request, 'trade2.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'tio': tio, 'jugador': jugador, 'max_madera': max_madera, 'max_metal': max_metal, 'numero_aldeanos': numero_aldeanos})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")



def trade2Complete(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()
		pruebax=jugador.coordinateX
		pruebay=jugador.coordinateY
		id_usuario=jugador.id

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------


		user = request.POST['idtio']

		costemadera=request.POST['rangeInput']
		costemetal=request.POST['rangeInput2']
		numero_aldeanos=request.POST['numero_aldeanos']



		if numero_aldeanos != 0 :

			#CONSULTA SACA LAS COORDENADAS DEL USUARIO ELEGIDO
			tio = Player.objects.get(id=user)
			coordenadaxuser = tio.coordinateX
			coordenadayuser = tio.coordinateY
			#pruebax
			#pruebay

			#CALCULAMOS LA DISTANCIA DE UNA ALDEA A OTRA
			
			distancia=pow(((pow((int(coordenadaxuser)-int(pruebax)),2))+(pow((int(coordenadayuser)-int(pruebay)),2))),0.5)
			tiempototal=int(distancia)*600
			tiempototaldoble=int(tiempototal)*2
			
			tiempo0=time.time()+int(tiempototal)
			tiempo1=time.time()+int(tiempototaldoble)


			#calculamos la cantidad actual que tiene
			madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
			metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal


			#SI LA MADERA QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE LA MADERA AL CAP
			if ((((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))>int(cap_madera)):
				kk=int(cap_madera)-int(costemadera);
				new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
				#new_entry.save()
			else:
				#SINO, QUITA EL COSTE A LA MADERA TOTAL
				madera=(((time.time()-int(ultima_conexion))*(float(produccion_hora_madera)/3600))+int(cantidad_madera))-int(costemadera);
				new_entry = Sawmill.objects.filter(player_id=request.session['playerID']).update(quantity=madera)
				#new_entry.save()

			#SI EL METAL QUE TIENE ES MAYOR QUE EL CAP, QUITA EL COSTE DE EL METAL AL CAP
			if ((((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+int(cantidad_metal))>int(cap_metal)):
				kk=int(cap_metal)-int(costemetal);
				new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=kk)
				#new_entry.save()
			else:
				#SINO, QUITA EL COSTE AL METAL TOTAL
				metal=(((time.time()-int(ultima_conexion))*(float(produccion_hora_metal)/3600))+int(cantidad_metal))-int(costemetal);
				new_entry = Mine.objects.filter(player_id=request.session['playerID']).update(quantity=metal)
				#new_entry.save()


			timeactualizado=time.time();
		
			#COMO HEMOS ACTUALIZADO LA CANTIDAD DE MADERA Y METAL, ACTUALIZAMOS EL CAMPO DE ULTIMA CONEXION
			new_entry = Player.objects.filter(id=request.session['playerID']).update(lastlogin=timeactualizado)
			#new_entry.save()


			#INSERTAMOS UN REGISTRO EN EVENTOATACAR POR ULTIMO
			#IDA
			new_entry = Event_trade(player_id=jugador.id, time=tiempo0, procesed=0, player_victim_id=tio.id, workers=numero_aldeanos, wood=costemadera, iron=costemetal, back_time=0)
			new_entry.save()
			
			#VUELTA
			new_entry = Event_trade(player_id=jugador.id, time=tiempo1, procesed=0, player_victim_id=tio.id, workers=numero_aldeanos, wood=costemadera, iron=costemetal, back_time=1)
			new_entry.save()
			
			
			#SACAMOS DE LA TABLA EJERCITO LAS UNIDADES UTILIZADAS
			new_entry = Army.objects.filter(player_id=request.session['playerID']).update(unit99=F('unit99') - numero_aldeanos)

			return render(request, 'trade2Complete.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'tio': tio, 'jugador': jugador})

		else:
			return HttpResponseRedirect("/game/world")
	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def messages(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()
		pruebax=jugador.coordinateX
		pruebay=jugador.coordinateY
		id_usuario=jugador.id

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		return render(request, 'messages.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def messagesOutbox(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()
		pruebax=jugador.coordinateX
		pruebay=jugador.coordinateY
		id_usuario=jugador.id

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------


		
		try:
			mensajes = Message.objects.filter(transmitter_id=request.session['playerID']).order_by('time').reverse()
		except Message.DoesNotExist:
			mensajes = None

		

		return render(request, 'messagesOutbox.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'mensajes': mensajes})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")



def messagesOutbox2(request, id):


	try:

		if 'playerID' in request.session:
			#--------------------------------------------
			nombreusuario=request.session['player']
			faccionusuario=request.session['faction']
			#cargamos los recursos del usuario
			jugador = Player.objects.get(name=request.session['player'])
			ultima_conexion=jugador.lastlogin
			nombrepoblado=jugador.town.upper()
			pruebax=jugador.coordinateX
			pruebay=jugador.coordinateY
			id_usuario=jugador.id

			aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
			produccion_hora_madera = aserradero.production_hour
			cantidad_madera = aserradero.quantity
			cap_madera = aserradero.capacity

			mina = Mine.objects.get(player_id=request.session['playerID'])
			produccion_hora_metal = mina.production_hour
			cantidad_metal = mina.quantity
			cap_metal = mina.capacity

			granja = Farm.objects.get(player_id=request.session['playerID'])
			cantidad = granja.quantity
			capacidad = granja.capacity

			#calculamos la cantidad actual que tiene
			madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
			metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

			ratiosumamadera=float(produccion_hora_madera)/3600
			ratiosumametal=float(produccion_hora_metal)/3600

			#Cargamos las unidades que tiene el jugador
			ejercito = Army.objects.get(player_id=request.session['playerID'])
			unidad1=ejercito.unit1
			unidad2=ejercito.unit2
			unidad3=ejercito.unit3
			unidad4=ejercito.unit4
			unidad5=ejercito.unit5
			unidad6=ejercito.unit6
			unidad7=ejercito.unit7
			unidad8=ejercito.unit8
			unidad9=ejercito.unit9
			unidad10=ejercito.unit10
			unidad99=ejercito.unit99

			#leemos el fichero ejercito.txt para obtener el nombre de las unidades
			#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
			#lines = txtejercito.readlines()

			#lines[0].split(':')
			tiempotope=time.time();
			tiempotope2=time.time();
			tiempotope3=time.time();
			tiempotope4=time.time();
			edificioactualizado=0
			cantidad2=0
			vuelta3=0
			vuelta4=0
			#Miramos los contadores de los eventos
			try:
				eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_update.DoesNotExist:
				eventoactualiza = None
			if eventoactualiza != None:
				for x in eventoactualiza:
					tiempotope = eventoactualiza[0].time
					edificioactualizado = eventoactualiza[0].build

			try:
				eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_create.DoesNotExist:
				eventocrea = None
			if eventocrea != None:
				for x in eventocrea:
					tiempotope2 = x.time
					cantidad2 = x.quantity

			try:
				eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_atack.DoesNotExist:
				eventoataca = None
			if eventoataca != None:
				for x in eventoataca:
					tiempotope3 = x.time
					vuelta3 = x.back_time

			try:
				eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_trade.DoesNotExist:
				eventocomercia = None
			if eventocomercia != None:
				for x in eventocomercia:
					tiempotope4 = x.time
					vuelta4 = x.back_time


			#calculamos tiempos
			tiempoactual=time.time();
			
			
			restante=tiempotope-tiempoactual;
			restante2=tiempotope2-tiempoactual;
			restante3=tiempotope3-tiempoactual;
			restante4=tiempotope4-tiempoactual;
				
			#------------------------------

			idmensaje= id
			
			try:
				mensajes = Message.objects.get(id=idmensaje)
			except Message.DoesNotExist:
				mensajes = None

			new_entry = Message.objects.filter(id=idmensaje).update(read=1)
			

			return render(request, 'messagesOutbox2.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'mensajes': mensajes})

		else:
			#El usuario no esta logueado
			return HttpResponseRedirect("/accounts/login")

	except Message.DoesNotExist:
		raise Http404



def messagesInbox(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()
		pruebax=jugador.coordinateX
		pruebay=jugador.coordinateY
		id_usuario=jugador.id

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------


		
		try:
			mensajes = Message.objects.filter(receiver_id=request.session['playerID']).order_by('time').reverse()
		except Message.DoesNotExist:
			mensajes = None

		

		return render(request, 'messagesInbox.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'mensajes': mensajes})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")



def messagesInbox2(request, id):

	try:

		if 'playerID' in request.session:
			#--------------------------------------------
			nombreusuario=request.session['player']
			faccionusuario=request.session['faction']
			#cargamos los recursos del usuario
			jugador = Player.objects.get(name=request.session['player'])
			ultima_conexion=jugador.lastlogin
			nombrepoblado=jugador.town.upper()
			pruebax=jugador.coordinateX
			pruebay=jugador.coordinateY
			id_usuario=jugador.id

			aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
			produccion_hora_madera = aserradero.production_hour
			cantidad_madera = aserradero.quantity
			cap_madera = aserradero.capacity

			mina = Mine.objects.get(player_id=request.session['playerID'])
			produccion_hora_metal = mina.production_hour
			cantidad_metal = mina.quantity
			cap_metal = mina.capacity

			granja = Farm.objects.get(player_id=request.session['playerID'])
			cantidad = granja.quantity
			capacidad = granja.capacity

			#calculamos la cantidad actual que tiene
			madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
			metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

			ratiosumamadera=float(produccion_hora_madera)/3600
			ratiosumametal=float(produccion_hora_metal)/3600

			#Cargamos las unidades que tiene el jugador
			ejercito = Army.objects.get(player_id=request.session['playerID'])
			unidad1=ejercito.unit1
			unidad2=ejercito.unit2
			unidad3=ejercito.unit3
			unidad4=ejercito.unit4
			unidad5=ejercito.unit5
			unidad6=ejercito.unit6
			unidad7=ejercito.unit7
			unidad8=ejercito.unit8
			unidad9=ejercito.unit9
			unidad10=ejercito.unit10
			unidad99=ejercito.unit99

			#leemos el fichero ejercito.txt para obtener el nombre de las unidades
			#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
			#lines = txtejercito.readlines()

			#lines[0].split(':')
			tiempotope=time.time();
			tiempotope2=time.time();
			tiempotope3=time.time();
			tiempotope4=time.time();
			edificioactualizado=0
			cantidad2=0
			vuelta3=0
			vuelta4=0
			#Miramos los contadores de los eventos
			try:
				eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_update.DoesNotExist:
				eventoactualiza = None
			if eventoactualiza != None:
				for x in eventoactualiza:
					tiempotope = eventoactualiza[0].time
					edificioactualizado = eventoactualiza[0].build

			try:
				eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_create.DoesNotExist:
				eventocrea = None
			if eventocrea != None:
				for x in eventocrea:
					tiempotope2 = x.time
					cantidad2 = x.quantity

			try:
				eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_atack.DoesNotExist:
				eventoataca = None
			if eventoataca != None:
				for x in eventoataca:
					tiempotope3 = x.time
					vuelta3 = x.back_time

			try:
				eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_trade.DoesNotExist:
				eventocomercia = None
			if eventocomercia != None:
				for x in eventocomercia:
					tiempotope4 = x.time
					vuelta4 = x.back_time


			#calculamos tiempos
			tiempoactual=time.time();
			
			
			restante=tiempotope-tiempoactual;
			restante2=tiempotope2-tiempoactual;
			restante3=tiempotope3-tiempoactual;
			restante4=tiempotope4-tiempoactual;
				
			#------------------------------

			idmensaje= id
			
			try:
				mensajes = Message.objects.get(id=idmensaje)
			except Message.DoesNotExist:
				mensajes = None


			new_entry = Message.objects.filter(id=idmensaje).update(read=1)


			return render(request, 'messagesInbox2.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'mensajes': mensajes})

		else:
			#El usuario no esta logueado
			return HttpResponseRedirect("/accounts/login")

	except Message.DoesNotExist:
		raise Http404



def messagesSend(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------


		user = 1

		jugadorestodosbuenos=[]
		jugadorestodos = Player.objects.all()
		if jugadorestodos != None:
			for x in jugadorestodos:
				jugadorestodosbuenos.append(x.name)

		return render(request, 'messagesSend.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'jugador': jugador, 'jugadorestodosbuenos': jugadorestodosbuenos, 'user': user})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")



def messagesSendComplete(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------


		user = request.POST['userid']

		receptor=request.POST['receptor'];
		asunto=request.POST['asunto'];
		contenido=request.POST['contenido'];

		tiemponow=time.time()
		datenow=datetime.datetime.now()


		jugadoridreceptor = Player.objects.get(name=receptor)
		jugadoridreceptorbueno=jugadoridreceptor.id

		new_entry = Message(transmitter_id=jugador.id, receiver_id=jugadoridreceptorbueno, title=asunto, text=contenido, read=0, date=datenow, time=tiemponow)
		new_entry.save()
		

		return render(request, 'messagesSendComplete.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'jugador': jugador})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def reports(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()
		pruebax=jugador.coordinateX
		pruebay=jugador.coordinateY
		id_usuario=jugador.id

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		return render(request, 'reports.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")


def reportsBattle(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()
		pruebax=jugador.coordinateX
		pruebay=jugador.coordinateY
		id_usuario=jugador.id

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------


		
		try:
			mensajes = Report_battle.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Message.DoesNotExist:
			mensajes = None

		

		return render(request, 'reportsBattle.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'mensajes': mensajes})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")




def reportsBattle2(request, id):

	try:

		if 'playerID' in request.session:
			#--------------------------------------------
			nombreusuario=request.session['player']
			faccionusuario=request.session['faction']
			#cargamos los recursos del usuario
			jugador = Player.objects.get(name=request.session['player'])
			ultima_conexion=jugador.lastlogin
			nombrepoblado=jugador.town.upper()
			pruebax=jugador.coordinateX
			pruebay=jugador.coordinateY
			id_usuario=jugador.id

			aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
			produccion_hora_madera = aserradero.production_hour
			cantidad_madera = aserradero.quantity
			cap_madera = aserradero.capacity

			mina = Mine.objects.get(player_id=request.session['playerID'])
			produccion_hora_metal = mina.production_hour
			cantidad_metal = mina.quantity
			cap_metal = mina.capacity

			granja = Farm.objects.get(player_id=request.session['playerID'])
			cantidad = granja.quantity
			capacidad = granja.capacity

			#calculamos la cantidad actual que tiene
			madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
			metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

			ratiosumamadera=float(produccion_hora_madera)/3600
			ratiosumametal=float(produccion_hora_metal)/3600

			#Cargamos las unidades que tiene el jugador
			ejercito = Army.objects.get(player_id=request.session['playerID'])
			unidad1=ejercito.unit1
			unidad2=ejercito.unit2
			unidad3=ejercito.unit3
			unidad4=ejercito.unit4
			unidad5=ejercito.unit5
			unidad6=ejercito.unit6
			unidad7=ejercito.unit7
			unidad8=ejercito.unit8
			unidad9=ejercito.unit9
			unidad10=ejercito.unit10
			unidad99=ejercito.unit99

			#leemos el fichero ejercito.txt para obtener el nombre de las unidades
			#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
			#lines = txtejercito.readlines()

			#lines[0].split(':')
			tiempotope=time.time();
			tiempotope2=time.time();
			tiempotope3=time.time();
			tiempotope4=time.time();
			edificioactualizado=0
			cantidad2=0
			vuelta3=0
			vuelta4=0
			#Miramos los contadores de los eventos
			try:
				eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_update.DoesNotExist:
				eventoactualiza = None
			if eventoactualiza != None:
				for x in eventoactualiza:
					tiempotope = eventoactualiza[0].time
					edificioactualizado = eventoactualiza[0].build

			try:
				eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_create.DoesNotExist:
				eventocrea = None
			if eventocrea != None:
				for x in eventocrea:
					tiempotope2 = x.time
					cantidad2 = x.quantity

			try:
				eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_atack.DoesNotExist:
				eventoataca = None
			if eventoataca != None:
				for x in eventoataca:
					tiempotope3 = x.time
					vuelta3 = x.back_time

			try:
				eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_trade.DoesNotExist:
				eventocomercia = None
			if eventocomercia != None:
				for x in eventocomercia:
					tiempotope4 = x.time
					vuelta4 = x.back_time


			#calculamos tiempos
			tiempoactual=time.time();
			
			
			restante=tiempotope-tiempoactual;
			restante2=tiempotope2-tiempoactual;
			restante3=tiempotope3-tiempoactual;
			restante4=tiempotope4-tiempoactual;
				
			#------------------------------

			idmensaje= id
			
			try:
				mensajes = Report_battle.objects.get(id=idmensaje)
			except Message.DoesNotExist:
				mensajes = None


			return render(request, 'reportsBattle2.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'mensajes': mensajes})

		else:
			#El usuario no esta logueado
			return HttpResponseRedirect("/accounts/login")

	except Report_battle.DoesNotExist:
		raise Http404


def reportsTrade(request):


	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()
		pruebax=jugador.coordinateX
		pruebay=jugador.coordinateY
		id_usuario=jugador.id

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------


		
		try:
			mensajes = Report_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Message.DoesNotExist:
			mensajes = None

		

		return render(request, 'reportsTrade.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'mensajes': mensajes})

	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")



def reportsTrade2(request, id):

	try:
		if 'playerID' in request.session:
			#--------------------------------------------
			nombreusuario=request.session['player']
			faccionusuario=request.session['faction']
			#cargamos los recursos del usuario
			jugador = Player.objects.get(name=request.session['player'])
			ultima_conexion=jugador.lastlogin
			nombrepoblado=jugador.town.upper()
			pruebax=jugador.coordinateX
			pruebay=jugador.coordinateY
			id_usuario=jugador.id

			aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
			produccion_hora_madera = aserradero.production_hour
			cantidad_madera = aserradero.quantity
			cap_madera = aserradero.capacity

			mina = Mine.objects.get(player_id=request.session['playerID'])
			produccion_hora_metal = mina.production_hour
			cantidad_metal = mina.quantity
			cap_metal = mina.capacity

			granja = Farm.objects.get(player_id=request.session['playerID'])
			cantidad = granja.quantity
			capacidad = granja.capacity

			#calculamos la cantidad actual que tiene
			madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
			metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

			ratiosumamadera=float(produccion_hora_madera)/3600
			ratiosumametal=float(produccion_hora_metal)/3600

			#Cargamos las unidades que tiene el jugador
			ejercito = Army.objects.get(player_id=request.session['playerID'])
			unidad1=ejercito.unit1
			unidad2=ejercito.unit2
			unidad3=ejercito.unit3
			unidad4=ejercito.unit4
			unidad5=ejercito.unit5
			unidad6=ejercito.unit6
			unidad7=ejercito.unit7
			unidad8=ejercito.unit8
			unidad9=ejercito.unit9
			unidad10=ejercito.unit10
			unidad99=ejercito.unit99

			#leemos el fichero ejercito.txt para obtener el nombre de las unidades
			#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
			#lines = txtejercito.readlines()

			#lines[0].split(':')
			tiempotope=time.time();
			tiempotope2=time.time();
			tiempotope3=time.time();
			tiempotope4=time.time();
			edificioactualizado=0
			cantidad2=0
			vuelta3=0
			vuelta4=0
			#Miramos los contadores de los eventos
			try:
				eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_update.DoesNotExist:
				eventoactualiza = None
			if eventoactualiza != None:
				for x in eventoactualiza:
					tiempotope = eventoactualiza[0].time
					edificioactualizado = eventoactualiza[0].build

			try:
				eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_create.DoesNotExist:
				eventocrea = None
			if eventocrea != None:
				for x in eventocrea:
					tiempotope2 = x.time
					cantidad2 = x.quantity

			try:
				eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_atack.DoesNotExist:
				eventoataca = None
			if eventoataca != None:
				for x in eventoataca:
					tiempotope3 = x.time
					vuelta3 = x.back_time

			try:
				eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
			except Event_trade.DoesNotExist:
				eventocomercia = None
			if eventocomercia != None:
				for x in eventocomercia:
					tiempotope4 = x.time
					vuelta4 = x.back_time


			#calculamos tiempos
			tiempoactual=time.time();
			
			
			restante=tiempotope-tiempoactual;
			restante2=tiempotope2-tiempoactual;
			restante3=tiempotope3-tiempoactual;
			restante4=tiempotope4-tiempoactual;
				
			#------------------------------

			idmensaje= id
			
			try:
				mensajes = Report_trade.objects.get(id=idmensaje)
			except Message.DoesNotExist:
				mensajes = None


			return render(request, 'reportsTrade2.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'mensajes': mensajes})

		else:
			#El usuario no esta logueado
			return HttpResponseRedirect("/accounts/login")

	except Report_trade.DoesNotExist:
		raise Http404


def ranking(request):

	if 'playerID' in request.session:
		#--------------------------------------------
		nombreusuario=request.session['player']
		faccionusuario=request.session['faction']
		#cargamos los recursos del usuario
		jugador = Player.objects.get(name=request.session['player'])
		ultima_conexion=jugador.lastlogin
		nombrepoblado=jugador.town.upper()
		pruebax=jugador.coordinateX
		pruebay=jugador.coordinateY
		id_usuario=jugador.id

		aserradero = Sawmill.objects.get(player_id=request.session['playerID'])
		produccion_hora_madera = aserradero.production_hour
		cantidad_madera = aserradero.quantity
		cap_madera = aserradero.capacity

		mina = Mine.objects.get(player_id=request.session['playerID'])
		produccion_hora_metal = mina.production_hour
		cantidad_metal = mina.quantity
		cap_metal = mina.capacity

		granja = Farm.objects.get(player_id=request.session['playerID'])
		cantidad = granja.quantity
		capacidad = granja.capacity

		#calculamos la cantidad actual que tiene
		madera=((time.time()-ultima_conexion)*(float(produccion_hora_madera)/3600))+cantidad_madera
		metal=((time.time()-ultima_conexion)*(float(produccion_hora_metal)/3600))+cantidad_metal

		ratiosumamadera=float(produccion_hora_madera)/3600
		ratiosumametal=float(produccion_hora_metal)/3600

		#Cargamos las unidades que tiene el jugador
		ejercito = Army.objects.get(player_id=request.session['playerID'])
		unidad1=ejercito.unit1
		unidad2=ejercito.unit2
		unidad3=ejercito.unit3
		unidad4=ejercito.unit4
		unidad5=ejercito.unit5
		unidad6=ejercito.unit6
		unidad7=ejercito.unit7
		unidad8=ejercito.unit8
		unidad9=ejercito.unit9
		unidad10=ejercito.unit10
		unidad99=ejercito.unit99

		#leemos el fichero ejercito.txt para obtener el nombre de las unidades
		#txtejercito = open('juego/static/ficheros/ejercito.txt', 'r')
		#lines = txtejercito.readlines()

		#lines[0].split(':')
		tiempotope=time.time();
		tiempotope2=time.time();
		tiempotope3=time.time();
		tiempotope4=time.time();
		edificioactualizado=0
		cantidad2=0
		vuelta3=0
		vuelta4=0
		#Miramos los contadores de los eventos
		try:
			eventoactualiza = Event_update.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_update.DoesNotExist:
			eventoactualiza = None
		if eventoactualiza != None:
			for x in eventoactualiza:
				tiempotope = eventoactualiza[0].time
				edificioactualizado = eventoactualiza[0].build

		try:
			eventocrea = Event_create.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_create.DoesNotExist:
			eventocrea = None
		if eventocrea != None:
			for x in eventocrea:
				tiempotope2 = x.time
				cantidad2 = x.quantity

		try:
			eventoataca = Event_atack.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_atack.DoesNotExist:
			eventoataca = None
		if eventoataca != None:
			for x in eventoataca:
				tiempotope3 = x.time
				vuelta3 = x.back_time

		try:
			eventocomercia = Event_trade.objects.filter(player_id=request.session['playerID']).order_by('time').reverse()
		except Event_trade.DoesNotExist:
			eventocomercia = None
		if eventocomercia != None:
			for x in eventocomercia:
				tiempotope4 = x.time
				vuelta4 = x.back_time


		#calculamos tiempos
		tiempoactual=time.time();
		
		
		restante=tiempotope-tiempoactual;
		restante2=tiempotope2-tiempoactual;
		restante3=tiempotope3-tiempoactual;
		restante4=tiempotope4-tiempoactual;
			
		#------------------------------

		ejercitos=Army.objects.all()
		devuelto=[]
		devueltobueno=[]
		for x in ejercitos:
			juplayers = Player.objects.get(id=x.player_id)
			total= x.unit1+x.unit2+x.unit3+x.unit4+x.unit5+x.unit6+x.unit7+x.unit8+x.unit9+x.unit10
			devuelto.append(juplayers.name)
			devuelto.append(int(total))
			devueltobueno.append(devuelto)
			devuelto=[]

		#devueltobueno.sort(key=lambda x: x.1, reverse=True)
		
		devueltobueno.sort(key=lambda x: x[1], reverse=True)
		
		return render(request, 'ranking.html', {'ratiosumamadera': ratiosumamadera, 'ratiosumametal': ratiosumametal, 'cap_madera': cap_madera, 'madera': madera, 'cap_metal': cap_metal, 'metal': metal, 'cantidad': cantidad, 'capacidad': capacidad, 'nombreusuario': nombreusuario, 'nombrepoblado': nombrepoblado, 'faccionusuario': faccionusuario, 'unidad1': unidad1, 'unidad2': unidad2, 'unidad3': unidad3, 'unidad4': unidad4, 'unidad5': unidad5, 'unidad6': unidad6, 'unidad7': unidad7, 'unidad8': unidad8, 'unidad9': unidad9, 'unidad10': unidad10, 'unidad99': unidad99, 'restante': restante, 'restante2': restante2, 'restante3': restante3, 'restante4': restante4, 'edificioactualizado': edificioactualizado, 'cantidad2': cantidad2, 'vuelta3': vuelta3, 'vuelta4': vuelta4, 'devueltobueno': devueltobueno})

		
	else:
		#El usuario no esta logueado
		return HttpResponseRedirect("/accounts/login")



def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response