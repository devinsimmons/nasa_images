from bs4 import BeautifulSoup as bs
import urllib
import os.path 
import json



class nasa_images:
    
    def __init__(self, num_images, outfolder):
        #number of images desired
        self.num_images = num_images
        #folder to insert the images
        self.outfolder = outfolder

    def download(self):
        site = 'https://earthobservatory.nasa.gov/images'

        page = urllib.request.urlopen(site).read()
        soup = bs(page, features= "html.parser")
        soup.prettify()
        
        imgs = soup.findAll('div', {'class': 'thumbnail-image'})
        
        counter = 0
        
        for img in imgs:
            
            if counter == self.num_images:
                return True
                break
            
            page = urllib.request.urlopen(site + img.a.get('href')[7:])
            soup = bs(page, features = 'html.parser')
            soup.prettify()
            
            map_img = soup.findAll('div', {'class': 'panel-image'})[0]
            
            #handles exception to the typical format. if not true, no file is downloaded
            if map_img.a:
                filename =  self.outfolder + map_img.a.get('href').split('/')[-1]

                if not os.path.exists(filename):
                    urllib.request.urlretrieve(map_img.a.get('href'), filename)
                    counter += 1
        
        #scrolling further through the webpage to get more images
        #each page contains five images
        for i in range(2, (self.num_images - counter)//5 + 1):
            site = 'https://earthobservatory.nasa.gov/topic/image-of-the-day/getRecords?page=' + str(i)
            page = urllib.request.urlopen(site)
            data = json.load(page)
            
            #looping through dictionary entry, which contains details that let me
            #load each post
            for i in data['data']:
                slug = i['slug'].split('/')[-1]
                link = 'https://earthobservatory.nasa.gov/images/' + str(i['id']) + '/' + slug

                page = urllib.request.urlopen(link)
                
                soup = bs(page, features = 'html.parser')
                soup.prettify()
                
                map_img = soup.findAll('div', {'class': 'panel-image'})[0]
                #handles exceptions to the normal format
                if map_img.a:
                    filename = self.outfolder + map_img.a.get('href').split('/')[-1]
                
                    if not os.path.exists(filename):
                        urllib.request.urlretrieve(map_img.a.get('href'), filename)

images = nasa_images(20, r"C:\Users\devin.simmons.ctr\Desktop\projects\nasa_images\images\\")
images.download()