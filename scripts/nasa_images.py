from bs4 import BeautifulSoup as bs
import urllib
import os.path 
import json

site = 'https://earthobservatory.nasa.gov/images'

page = urllib.request.urlopen(site).read()
soup = bs(page, features= "html.parser")
soup.prettify()

imgs = soup.findAll('div', {'class': 'thumbnail-image'})


for img in imgs:
    page = urllib.request.urlopen(site + img.a.get('href')[7:])
    soup = bs(page, features = 'html.parser')
    soup.prettify()
    
    map_img = soup.findAll('div', {'class': 'panel-image'})[0]
    filename = r"C:\Users\devin.simmons.ctr\Desktop\projects\nasa_images\images\\" + map_img.a.get('href').split('/')[-1]
    
    if not os.path.exists(filename):
        urllib.request.urlretrieve(map_img.a.get('href'), filename)
                                
#scrolling further through the webpage to get more images
for i in range(3, 30):
    site = 'https://earthobservatory.nasa.gov/topic/image-of-the-day/getRecords?page=' + str(i)
    page = urllib.request.urlopen(site)
    data = json.load(page)
    
    #looping through dictionary entry, which contains details that let me
    #load each post
    for i in data['data']:
        slug = i['slug'].split('/')[-1]
        link = 'https://earthobservatory.nasa.gov/images/' + str(i['id']) + '/' + slug
        
        print(link)
        page = urllib.request.urlopen(link)
        
        soup = bs(page, features = 'html.parser')
        soup.prettify()
        
        map_img = soup.findAll('div', {'class': 'panel-image'})[0]
        if map_img.a:
            filename = r"C:\Users\devin.simmons.ctr\Desktop\projects\nasa_images\images\\" + map_img.a.get('href').split('/')[-1]
        
        if not os.path.exists(filename):
            urllib.request.urlretrieve(map_img.a.get('href'), filename)