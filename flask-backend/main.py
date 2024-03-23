from flask import Flask
from flask_restful import Resource, Api
import requests
from bs4 import BeautifulSoup
import sys
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

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
        return {'images': getURLNaruto(name)}

api.add_resource(Images, '/<name>')
 
if __name__ == '__main__':
    app.run(debug=True)
