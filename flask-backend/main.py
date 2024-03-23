import requests
from bs4 import BeautifulSoup
import sys
#hello
url = 'https://naruto.fandom.com/wiki/Naruto_Uzumaki'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

sys.stdout.reconfigure(encoding='utf-8')
images = []

for link in soup.find_all('a', href=True):
    if link['href'].startswith('http'):
        images.append(link['href'])


print(images)
