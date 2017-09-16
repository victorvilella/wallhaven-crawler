from threading import Thread
from time import sleep
from bs4 import BeautifulSoup
import os
import requests


class Downloader(Thread):
    def __init__(self, query, location):
        Thread.__init__(self)
        self.q = query
        self.location = location
        pass

    def run(self):
        self.query(self.q)
        sleep(60)

    def query(self, query):
        page = 1
        thumbs = []
        while(True):
            r = requests.get("https://alpha.wallhaven.cc/search?q=" + query.replace(" ", "+") + "&page=" + str(page))
            results = BeautifulSoup(r.content, "html.parser").find_all("a", {"class": "preview"})
            r.close()
            if results.__len__() > 0:
                for result in results:
                    thumbs.append(result)
            else:
                break
            page += 1
        print("Found " + str(thumbs.__len__()) + " results")
        for thumb in thumbs:
            link = thumb['href']
            self.downloadFile(link)


    def downloadFile(self, url):
        photo = BeautifulSoup(requests.get(url).text, "html.parser").find("img", {"id": "wallpaper"})["src"]
        if not os.path.isdir(self.location + self.q):
            os.mkdir(self.location + self.q)
        filename = self.location + self.q + '/' + photo.split("/")[-1]
        r = requests.get("https:"+ photo, stream=True)
        resource = r.content
        r.close()
        with open(filename, "wb") as wallpaper:
            wallpaper.write(resource)
            wallpaper.close()
            print("File " + filename + " saved!")

