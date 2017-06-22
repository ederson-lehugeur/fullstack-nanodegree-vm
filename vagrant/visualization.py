# -*- coding: UTF-8 -*-
# Visualização do banco de dados.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#firstResult = session.query(Restaurant).first()
# Mostra o endereço do objeto na memória.
#print firstResult
# Mostra o valor do campo nome da tabela Restaurant.
#print firstResult.name
# Selecionar todos os registros
print 'Restautantes'
items = session.query(Restaurant).all()
for item in items:
	print item.name
	
print 'Menus'
items = session.query(MenuItem).all()
for item in items:
	print item.name, item.description, item.price, item.course