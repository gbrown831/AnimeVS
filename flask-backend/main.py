from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import requests
from bs4 import BeautifulSoup
import sys
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import pandas as pd
import random
from sqlalchemy_serializer import SerializerMixin


#------------------------------------------------------------- App Configuration -----------------------------------------------------------#
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

# ------------------------------------------------------------ Flask Models ----------------------------------------------------------------#

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


#-------------------------------------------------------- Intermediate Functions----------------------------------------------------------#

def getURLNaruto(url): #Works only for Naruto
    """
    Web scraping function specifically for Naruto Characters
    using the following source: https://naruto.fandom.com/wiki/Narutopedia
    @parem url The url of the specific random Naruto character selected
    """

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

def getURL(url): #Works for DragonBall, JJK, and OnePiece
    """
    Web scraping function for One Punch Man, JJK, and One Piece,
    using the following respective sources:
    https://onepunchman.fandom.com/wiki/One-Punch_Man_Wiki
    https://jujutsu-kaisen.fandom.com/wiki/Jujutsu_Kaisen_Wiki
    https://onepiece.fandom.com/wiki/One_Piece_Wiki

    @param url The url for the random anime character selected
    """

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


#------------------------------------------------------------ Middleware -------------------------------------------------------------------#

class Images(Resource):
    def get(self):
        """
        Retrieves the information for two random characters from the database
        """

        #generates new random IDs
        characters = db.session.execute(db.select(Character))
        num_characters = len(characters.all())

        #generate two random numbers from 0 to num_characters
        #char1 = query where character ID is random number 1
        #char2 = query where character ID is random number 2
        rand1 = -1
        rand2 = -1
        while rand1 == rand2:
            rand1 = random.randint(1, num_characters-1)
            rand2 = random.randint(1, num_characters-1)
        char1 = Character.query.get(rand1)
        char2 = Character.query.get(rand2)
        
        # Decide whether to use the Naruto or the
        # Default web scrapper
        if char1.show == "Naruto":
            char1_url = getURLNaruto(char1.url)
        else:
            char1_url = getURL(char1.url)
        
        if char2.show == "Naruto":
            char2_url = getURLNaruto(char2.url)
        else:
            char2_url = getURL(char2.url)

        return {
            'test': len(characters.all()),
            'char1': char1.to_dict(),
            'char2': char2.to_dict(),
            'char1_url': char1_url,
            'char2_url': char2_url,
        }
    
    def post(self):
        """
        Saves the users vote from the angular frontend into the database
        """

        # Processing the user's information from the frontend
        data = request.json
        char1num = data['char1_id']
        char2num = data['char2_id']
        winid = data['winner']
        switches = False
        
        # For a battle, the ID of the first character must be strictly less
        # than the ID of the second character for uniqueness of rooms.  Swap
        # the order of ID's if necessary
        if char2num < char1num:
            foo = char2num
            char2num = char1num
            char1num = foo
            switches = True

        # If a battle between the two characters already exists, increment the
        # votes for the winner.  Otherwise, create a new battle object between
        # the two characters
        try:
            battle = Battle.query.filter_by(char1_id = char1num, char2_id = char2num).first()
            if winid == char1num:
                battle.votes1 = battle.votes1 + 1
            else:
                battle.votes2 = battle.votes2 + 1
            context = {
                'votes1': battle.votes1,
                'votes2': battle.votes2,
                'switch': switches          
            }

        except:
            battles = db.session.execute(db.select(Battle))
            if winid == char1num:       
                # new_battle = Battle(id=len(battles.all()), char1_id = char1num, char2_id = char2num, votes1=1,votes2=0)
                new_battle = Battle(id=len(battles.all()), char1_id = char1num, char2_id = char2num, votes1=random.randint(1, 10),votes2=random.randint(0, 10))
            else:
                # new_battle = Battle(id=len(battles.all()), char1_id = char1num, char2_id = char2num, votes1=0,votes2=1)
                new_battle = Battle(id=len(battles.all()), char1_id = char1num, char2_id = char2num, votes1=random.randint(0, 10),votes2=random.randint(1, 10))
            
            db.session.add(new_battle)

            context = {
                'votes1': new_battle.votes1,
                'votes2': new_battle.votes2,
                'switch': switches
            }
        
        db.session.commit()
        return context
    
api.add_resource(Images, '/')


if __name__ == '__main__':
    app.run(debug=True)

    ## Used to create the database
    # with app.test_request_context():
    #  db.create_all()

    ## Used to initiate values in the characters table
    # with app.app_context():
    #     for index, row in animeCharacters.iterrows():
    #         new_char = Character(name = row['name'], show = row['show'], url = row['url'])
    #         db.session.add(new_char)
    #         db.session.commit()
