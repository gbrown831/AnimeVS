from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#for reading the spreadsheet
import pandas as pd

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension


animeCharacters = pd.read_csv('./AnimeCharacters.csv')


# #Create database names sqlitedbs
# engine = create_engine('sqlite:///C:\\sqlitedbs\\database.db')

# #declare the base. Not sure if this is needed
Base = declarative_base()

#character table
class Character(db.Model):

    __tablename__ = 'characters'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True, nullable=False)
    show = db.Column(String(50), unique=True, nullable=False)
    url = db.Column(String(50), unique=True, nullable=False)

#battle table
class Battle(db.Model):
    __tablename__ = 'battles'
    id = db.Column(Integer, primary_key=True)
    char1id = db.Column(Integer, primary_key=True)
    char2id = db.Column(Integer, primary_key=True)
    votes1 = db.Column(Integer, primary_key=True)
    votes2 = db.Column(Integer, primary_key=True)

# #puts both of the tables into the database
# Base.metadata.create_all(engine)

# #read data from csv file, create character objects, and insert them into the table
# Session = sessionmaker(bind=engine)
# session = Session()

# for index, row in animeCharacters.iterrows():
#     new_char = Character(charName = row['name'], charShow = row['show'],charShowURL = row['url'])
#     session.add(new_char)
#     session.commit()
# session.close()

with app.app_context():
    db.create_all()








