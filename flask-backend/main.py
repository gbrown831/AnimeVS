from flask import Flask
from flask_restful import Resource, Api
import requests
from bs4 import BeautifulSoup
import sys

app = Flask(__name__)
api = Api(app)

def getURL(name):
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
        
        # Print the href attribute of each <a> element found
        for a_element in a_elements_inside_class:
            if a_element['href'].startswith('http'):
                url_list.append(a_element['href'])

    return url_list

class Images(Resource):
    def get(self, name):
        return {'images': getURL(name.split(' ').join('_'))}

api.add_resource(Images, '/<str:name>')

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
    app.run(debug=True)
