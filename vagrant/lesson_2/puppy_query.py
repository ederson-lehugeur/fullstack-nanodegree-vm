# -*- coding: UTF-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from puppies import Base, Puppy, Shelter
#from flask.ext.sqlalchemy import SQLAlchemy
import datetime

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def query_1():
	# 1. Consulta todos os cachorros e retorna os resultados em ordem alfabética ascendente.
	result = session.query(Puppy.name).order_by(Puppy.name.asc()).all()
	
	for item in result:
		print item[0]
		
def query_2():
	# 2. Consulta todos os cachorros com menos de 6 meses organizados pelo mais novo primeiro.
	today = datetime.date.today()
	if passesLeapDay(today):
		sixMonthsAgo = today - datetime.timedelta(days = 183)
	else:
		sixMonthsAgo = today - datetime.timedelta(days = 182)
	result = session.query(Puppy.name, Puppy.dateOfBirth)\
		.filter(Puppy.dateOfBirth >= sixMonthsAgo)\
		.order_by(Puppy.dateOfBirth.desc())

	for item in result:
		print "{name}: {dob}".format(name = item[0], dob=item[1])

def query_3():
	# 3. Consulta todos os cachorros por peso ascendente.
	result = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight.asc()).all()

	for item in result:
		print item[0], item[1]

def query_4():
	# 4. Consulta todos os cachorros agrupados pelo abrigo em que estão hospedados.
	#result = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
	result = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()

	for item in result:
		print item[0].id, item[0].name, item[1]

def query_5():
	# 5. Consulta todos os nomes dos cachorros pelo abrigo em que estão hospedados.
	result = session.query(Shelter, Puppy).filter(Shelter.id == Puppy.shelter_id).order_by(Shelter.id, Puppy.name).all()

	for item in result:
		print item[0].id, item[0].name, item[1].name

def passesLeapDay(today):
	# Retorna verdadeiro se o mais recente dia 29 de fevereiro ocorreu após ou exatamente 183 dias atrás (366 / 2).
	thisYear = today.timetuple()[0]
	if isLeapYear(thisYear):
		sixMonthsAgo = today - datetime.timedelta(days = 183)
		leapDay = datetime.date(thisYear, 2, 29)
		return leapDay >= sixMonthsAgo
	else:
		return False

def isLeapYear(thisYear):
	'''
	Retorna verdadeiro se o ano atual é um ano bissexto. Implementado de acordo com a lógica em 
	https://en.wikipedia.org/wiki/Leap_year#Algorithm
	'''
	if thisYear % 4 != 0:
		return False
	elif thisYear % 100 != 0:
		return True
	elif thisYear % 400 != 0:
		return False
	else:
		return True

#query_1()
#query_2()
#query_3()
#query_4()
query_5()