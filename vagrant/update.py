# -*- coding: UTF-8 -*-
# Atualização do banco de dados.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
# Alterar o valor de um único registro.
'''
# O método one() acessa uma entrada no banco de dados.
urbanVeggieBurger = session.query(MenuItem).filter_by(id = 9).one()
#print urbanVeggieBurger.price
urbanVeggieBurger.price = '$2.99'
session.add(urbanVeggieBurger)
session.commit()
'''

# Altera o valor de todos os registros retornados.
for veggieBurger in veggieBurgers:
	if veggieBurger.price != '$2.99':
		veggieBurger.price = '$2.99'
		session.add(veggieBurger)
		session.commit()
		
for veggieBurger in veggieBurgers:
	print veggieBurger.id
	print veggieBurger.price
	print veggieBurger.restaurant.name
	print