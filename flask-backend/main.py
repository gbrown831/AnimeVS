from flask import Flask
from flask_restful import Resource, Api
import requests
from bs4 import BeautifulSoup
import sys
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import pandas as pd


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

def getURLNaruto(name): #Works only for Naruto
    url = 'https://naruto.fandom.com/wiki/' + name       #'https://naruto.fandom.com/wiki/Naruto_Uzumaki'

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

def getURL(name): #Works for DragonBall, JJK, and OnePiece
    url = 'https://dragonball.fandom.com/wiki/Vegeta' + name

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
    def get(self, name):
        #generates new random IDs
        characters = db.session.execute(db.select(Character))
        num_characters = len(characters.all())
        #generate two random numbers from 0 to num_characters
        #char1 = query where character ID is random number 1
        #char2 = query where character ID is random number 2

        return {
            'images': getURLNaruto(name),
            'test': len(characters.all())
            #char1: char1
            #char2: char2
        }
    

#character table
class Character(db.Model):

    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    show = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)

#battle table
class Battle(db.Model):
    __tablename__ = 'battles'
    id = db.Column(db.Integer, primary_key=True)
    char1id = db.Column(db.Integer, primary_key=True)
    char2id = db.Column(db.Integer, primary_key=True)
    votes1 = db.Column(db.Integer, primary_key=True)
    votes2 = db.Column(db.Integer, primary_key=True)

api.add_resource(Images, '/<name>')


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
