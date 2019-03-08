from threading import Thread
from time import sleep
from bs4 import BeautifulSoup
import os
import requests


class Downloader:
    results = None

    def __init__(self, query, location):
        self.q = query
        self.location = location
        pass

    def run(self):
        self.query(self.q)
        sleep(1)

    def query(self, query):
        page = 1
        thumbs = []
        print("Fetching results")
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
            print("Fetched {} results".format(len(thumbs)))
        print("Found " + str(thumbs.__len__()) + " results")
        self.results = thumbs
        self.handle()
        # for thumb in thumbs:
        #     link = thumb['href']
        #     self.downloadFile(link)

    def handle(self):
        while len(self.results):
            threads = []
            for i in range(0, 4):
                aux = self.results.pop()
                url = aux["href"]
                self.downloadFile(url)
                # t = Thread(target=self.downloadFile, args=(url,))
                # t.start()
                # threads.append(t)
            for i in range(0, 4):
                threads[i].join()
            


    def downloadFile(self, url):
        photo = BeautifulSoup(requests.get(url).text, "html.parser").find("img", {"id": "wallpaper"})["src"]
        aux = os.path.join(self.location + self.q)
        if not os.path.isdir(aux):
            os.mkdir(aux)
        filename = os.path.join(aux, photo.split("/")[-1])
        r = requests.get("https:"+ photo, stream=True)
        resource = r.content
        r.close()
        with open(filename, "wb") as wallpaper:
            wallpaper.write(resource)
            wallpaper.close()
            print("File " + filename + " saved!")

