from flask import Flask, request
from flask_restful import Resource, Api
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import requests
from bs4 import BeautifulSoup
import sys
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import pandas as pd
import random
from sqlalchemy_serializer import SerializerMixin



app = Flask(__name__)
CORS(app)
api = Api(app)

# create the extension
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
# create the app
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
animeCharacters = pd.read_csv('./AnimeCharacters.csv')
app.app_context()
# configure the SQLite database, relative to the app instance f

#character table
class Character(db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    show = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)

#battle table
class Battle(db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True)
    char1_id = db.Column(db.Integer, primary_key=True)
    char2_id = db.Column(db.Integer, primary_key=True)
    votes1 = db.Column(db.Integer, primary_key=True)
    votes2 = db.Column(db.Integer, primary_key=True)

def getURLNaruto(url): #Works only for Naruto

    url_list = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Set default encoding to UTF-8
    sys.stdout.reconfigure(encoding='utf-8')

    specific_class = soup.find_all(class_='smw-table-cell smwprops')

    # Iterate over each element with the specific class name
    for element in specific_class:
        # Find all <a> elements inside the current element
        a_elements_inside_class = element.find_all('a')
        
        # Return the href attribute of each <a> element found that starts with "http"
        #i.e returns image links
        for a_element in a_elements_inside_class:
            if a_element['href'].startswith('http'):
                str = a_element['href'][:a_element['href'].rfind('.png')+4]
                url_list.append(str)

    return url_list

def getURL(name, url): #Works for DragonBall, JJK, and OnePiece

    url_list = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Set default encoding to UTF-8
    sys.stdout.reconfigure(encoding='utf-8')

    specific_class = soup.find_all(class_='pi-item pi-image')
    # Iterate over each element with the specific class name
    for element in specific_class:
        # Find all <a> elements inside the current element
        a_elements_inside_class = element.find_all('a')
        
        # Return the href attribute of each <a> element found that starts with "http"
        #i.e returns image links
        for a_element in a_elements_inside_class:
            if a_element['href'].startswith('http'):
                str = a_element['href'][:a_element['href'].rfind('.png')+4]
                url_list.append(str)
    
    return url_list

class Images(Resource):
    def get(self):
        #generates new random IDs
        characters = db.session.execute(db.select(Character))
        num_characters = len(characters.all())
        #generate two random numbers from 0 to num_characters
        #char1 = query where character ID is random number 1
        #char2 = query where character ID is random number 2
        rand1 = -1
        rand2 = -1
        while rand1 == rand2:
            rand1 = random.randint(0, num_characters)
            rand2 = random.randint(0, num_characters)

        char1 = Character.query.get(rand1)
        char2 = Character.query.get(rand2)
        
        if char1.show == "Naruto":
            char1_url = getURLNaruto(char1.url)
        else:
            char1_url = getURL(char1.show, char1.url)
        
        if char2.show == "Naruto":
            char2_url = getURLNaruto(char2.url)
        else:
            char2_url = getURL(char2.show, char2.url)

        return {
            'test': len(characters.all()),
            'char1': char1.to_dict(),
            'char2': char2.to_dict(),
            'char1_url': char1_url,
            'char2_url': char2_url,
        }
    
    def post(self):
        #if char2id < char1id, char1id is char2id and char2id is char1id
        #for query for battle in database with the characters
        #if it is not there, make a battle and set the winners vote count to one
        #if it is there, increment the winners vote count
        #return voter counts
        data = request.json
        print(data)
        char1num = data['char1_id']
        char2num = data['char2_id']
        winid = data['winner']
        switches = False
        
        if char2num < char1num:
            foo = char2num
            char2num = char1num
            char1num = foo
            switches = True
        print(char1num, char2num, 'test')
        try:
            battle = Battle.query.filer_by(char1_id = char1num, char2_id = char2num)
            if winid == char1num:       
                battle.voter1 = battle.voter1 + 1
            else:
                battle.voter2 = battle.voter2 + 1

        except:
            battles = db.session.execute(db.select(Battle))
            if winid == char1num:       
                new_battle = Battle(id=len(battles.all()), char1_id = char1num, char2_id = char2num, votes1=1,votes2=0)
                print(new_battle.id)
            else:
                new_battle = Battle(id=len(battles.all()), char1_id = char1num, char2_id = char2num, votes1=0,votes2=1)
            
            db.session.add(new_battle)
            db.session.commit()
    
        return {
            'votes1': new_battle.votes1,
            'votes2': new_battle.votes2,
            'switch': switches
        }
    
api.add_resource(Images, '/')


# with app.test_request_context():
#      db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    # app.app_context()
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # with app.test_request_context():
    #  db.create_all()

    # with app.app_context():
    #     for index, row in animeCharacters.iterrows():
    #         new_char = Character(name = row['name'], show = row['show'], url = row['url'])
    #         db.session.add(new_char)
    #         db.session.commit()
