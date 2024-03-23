from flask import Flask
from flask_restful import Resource, Api
import requests  
from bs4 import BeautifulSoup
from urllib.request import urlopen

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self, name):
        r = requests.get("https://static.wikia.nocookie.net/naruto/images/4/42/Naruto_Part_III.png/revision/latest?cb=201801171035").content.decode('utf-8')
        return {"image":"https://static.wikia.nocookie.net/naruto/images/4/42/Naruto_Part_III.png/revision/latest?cb=201801171035"}

api.add_resource(HelloWorld, '/')

def scrape():
    url = "https://naruto.fandom.com/wiki/Naruto_Uzumaki"
    # r = requests.get(url).content.decode('utf-8')
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup.text

def get_image():
    with open("text.txt", "w", encoding="utf-8") as f:
        f.write(scrape("https://naruto.fandom.com/wiki/Naruto_Uzumaki"))

    # scrape("https://naruto.fandom.com/wiki/Naruto_Uzumaki")
    
if __name__ == '__main__':
    pass
    # with open("test.txt", "w", encoding="utf-8") as f:
    #     f.write(scrape())
