#!pip install bs4
#!pip install requests
#!pip install pandas
from bs4 import BeautifulSoup
import requests
import pandas as pd
URL="https://www.amazon.com/Sceptre-24-5-inch-DisplayPort-Speakers-C255B-FWT240/dp/B0BTKJFRDV/ref=sr_1_5?crid=30WTFDTNJHX98&dib=eyJ2IjoiMSJ9.Fsgv9OL72WlabSdiV43H9kKH-hD8lrhRgQzZEunkMujxgqWrs6uNY3zHxbTtkAT8c27xYNTmaUbwoJQSHqR5IMQAk5ALp_E0En_znLZl06ts9pgVwAU7CSG4gTgG4SuqRhgDlj4rQEIrb0UHhK3a1ajgrsW4kA79L24vUscE49rGXB-r49dp0IXCS-OXcoPjUzODrs-0ntoONQYM75IXzPGoE_grvaDEofV5-cdaGj0e7WNdUbUL4RdpItzqroCZ29WUGgAz-Foj10SPlH7nOd8cePphjeuXl9mynpPwVhACgt6SvMTE64I-bJMhSyQl6IMwzDns7jQrC_AARugUf6Wnzydjqp0UH4n60WF3eew2fLhYd73gPGJprUlTqxt-5-z9w0z8MbNFQ-emtwHgSC6n8WYj_58wVCo-lph_BkVZf2IkXTtztPvmc-kU8n8E.I75sPnnr6_KtS5NVrz4Umqm6snJWKoD52rWa1zi1lzg&dib_tag=se&keywords=gaming&qid=1739794432&sprefix=gaming%2Caps%2C340&sr=8-5&th=1"
#headers for requests
HEADERS = ({ 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36','Accept-Language':'en-US,en;q=0.5'})
#HTTP REQUEST
webpage=requests.get(URL,headers=HEADERS)
# soup object containg all data
soup=BeautifulSoup(webpage.content,"html.parser")
#fetch links as List of tag objects
links=soup.find_all("a",attrs={'class':'a-link-normal'})
link=links[0].get('href')
product_list="https://amazon.com"+link
product_list
#HTTP REQUEST
new_webpage=requests.get(URL,headers=HEADERS)
new_webpage
new_soup=BeautifulSoup(webpage.content,"html.parser")
new_soup
new_soup.find('span',attrs={"id":'productTitle'}).text.strip()
new_soup.find('span',attrs={"class":'a-price-whole'}).text.strip()
new_soup.find('span',attrs={"class":'a-icon-alt'}).text

