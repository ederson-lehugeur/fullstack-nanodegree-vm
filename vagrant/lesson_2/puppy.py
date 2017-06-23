# -*- coding: UTF-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Base declarativa.
# Cria uma classe base que nosso código de classe herdará.
Base = declarative_base()

class Shelter(Base):
	__tablename__ = 'shelter'
	id = Column(Integer, primary_key = True)
	name = Column(String(120), nullable = False)
	address = Column(String(120))
	city = Column(String(120))
	state = Column(String(120))
	zipCode = Column(String(10))
	website = Column(String(60))

class Puppy(Base):
	__tablename__ = 'puppy'
	id = Column(Integer, primary_key = True)
	name = Column(String(120), nullable = False)
	dataOfBirth = Column(Date)
	gender = Column(String(10), nullable = False)
	weight = Column(Numeric(10))
	picture = Column(String)
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)