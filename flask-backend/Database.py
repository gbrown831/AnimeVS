from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#for reading the spreadsheet
import pandas as pd

animeCharacters = pd.read_csv(r'C:\Users\gbrow\python\hoohacks\AnimeVS\AnimeCharacters.csv')


#Create database names sqlitedbs
engine = create_engine('sqlite:///C:\\sqlitedbs\\database.db')

#declare the base. Not sure if this is needed
Base = declarative_base()

#character table
class Characters(Base):

    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    show = Column(String(50), unique=True, nullable=False)
    url = Column(String(50), unique=True, nullable=False)

#battle table
class Battles(Base):
    __tablename__ = 'battles'
    id = Column(Integer, primary_key=True)
    char1id = Column(Integer, primary_key=True)
    char2id = Column(Integer, primary_key=True)
    votes1 = Column(Integer, primary_key=True)
    votes2 = Column(Integer, primary_key=True)

#puts both of the tables into the database
Base.metadata.create_all(engine)

#read data from csv file, create character objects, and insert them into the table
Session = sessionmaker(bind=engine)
session = Session()

for index, row in animeCharacters.iterrows():
    new_char = Characters(charName = row['name'], charShow = row['show'],charShowURL = row['url'])
    session.add(new_char)
    session.commit()
session.close()









