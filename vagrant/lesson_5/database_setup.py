# -*- coding: UTF-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Base declarativa.
# Cria uma classe base que nosso código de classe herdará.
Base = declarative_base()

class Restaurant(Base):
	__tablename__ = 'restaurant'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	
	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
		}

class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
	
    @property
    def serialize(self):
	    # Returns object data in easily serializeable format.
	    return {
            'id': self.id,
	        'name': self.name,
		    'description': self.description,
		    'price': self.price,
		    'course': self.course,
	    }

engine = create_engine('sqlite:///restaurant.db')
Base.metadata.create_all(engine)
