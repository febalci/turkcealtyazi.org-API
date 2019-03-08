# v0.2
# Düzeltme: Arama sayfası boş geldiğinde hata veriyor.
# Yapılacak: Dosya ve dizin isimlerini düzelt; orjinal ismi txt dosyası olarak dizinde tut
# v0.1
# İlk yükleme
import struct, os, sys
import urllib.request, urllib.parse
from urllib.error import URLError, HTTPError
import json
from bs4 import BeautifulSoup # pip3 install bs4 , pip3 install lxml
import PTN #pip3 install parse-torrent-name ,Windows: pip install https://github.com/divijbindlish/parse-torrent-name/archive/master.zip
from io import BytesIO
from zipfile import ZipFile
from rarfile import RarFile # pip3 install rarfile // unrar kurulu olmalı

# imdb koduna göre arama ?
# dizi sezon paketleri?

class MovieFile:

    subDomain = "https://www.turkcealtyazi.org"
    
    def __init__(self, fullpath, fullname):
        self.fileName = fullname
        self.movieName = os.path.splitext(fullname)[0] #Remove extension from name 
        self.filePath = fullpath
        self.seriesType = False
        parsedFile = PTN.parse(self.movieName)   
        self.parsedGroup, self.parsedSeason, self.parsedEpisode, self.parsedYear = "" ,"", "",""          
        parsedMovieName = parsedFile['title']
        print (self.fileName)
        match = input(parsedMovieName+'?')
        if match != "":
            parsedMovieName = match
        if 'group' in parsedFile:
            self.parsedGroup = parsedFile['group'].replace("[", "").replace("]", "") #Remove [] from YTS.AM
        if 'season' in parsedFile:
            self.seriesType = True
            self.parsedSeason = str(parsedFile['season']).rjust(2,'0')
            self.parsedEpisode = str(parsedFile['episode']).rjust(2,'0')
        if 'year' in parsedFile:
            self.parsedYear = parsedFile['year']
        self.findSub = parsedMovieName
        if self.parsedYear!="":
            self.findSub = self.findSub+' '+str(self.parsedYear)
        return
        
    def findTASubs(self):
        def printInfo():
            nonlocal saveCounter, counter
            print ("%2s" % counter +". :", end='')
            dil = link.find("div", class_="aldil").find("span").attrs['class'][0]
            print (dil[-2:].upper()+' | ', end='')
            print (link.find("div", class_="alcd").text.strip().replace("\n", "").replace("|", "")+' | ', end='')
            print (link.find("div", class_="algonderen").text+' | ', end='')
            print (link.find("div", class_="datediv").text+' | ', end='')
            print (link.find("div", class_="alfps").text+' | ', end='')
            ripdiv = link.find("div", class_="ripdiv").text.strip().replace(" ", "").replace("[", "").replace("]", "") #Remove [] from YTS.AM
            if self.parsedGroup in ripdiv:
                if saveCounter==None:
                    saveCounter = counter
            print (ripdiv)
            return

        self.findSub = urllib.parse.quote_plus(self.findSub)
        url = self.subDomain + '/find.php?cat=sub&find=%s'
        url = url % self.findSub
        counter = 1
        searchCounter = 1
        saveCounter = None
        found = False

        r = getWeb (url,'')
        source = BeautifulSoup(r,"lxml")    
        # Eğer <title> içinde arama varsa, bu sayfa başlığa göre birden fazla sayfa bulmuştur.
        if 'arama' in source.title.string:
            subTopTable = source.find_all("div",{"style": "float:left;width:450px;"})
            for link in subTopTable:
                print (str(searchCounter)+". : ", end='')
                print (link.text)
                print ('\n')
                searchCounter += 1
            if searchCounter>1:
                selectRight = input ('Lütfen Doğru Film/Dizinin Numarasını Giriniz (1):')
                if selectRight == "":
                    selectRight = '1'  
                r = getWeb (self.subDomain+subTopTable[int(selectRight)-1].find("a").attrs['href'],'')
                source = BeautifulSoup(r,"lxml")
        
        subTopTable = source.find("div",{"id": "altyazilar"})
        if subTopTable!=None:
            subTable = subTopTable.find_all("div",class_=None)
            del subTable[-1] #None class div 'lerden sonuncusunu sil, boş geliyor
            for link in subTable:
                if self.seriesType: #Dizi
                    aa = link.find("div", class_="alcd").text.strip().replace("\n", "").replace("|", "")
                    sezon = aa[1:3]
                    bolum = aa[-2:]
                    if (self.parsedSeason==sezon and self.parsedEpisode==bolum):
                        found = True
                        printInfo()
                    counter += 1

                else: #Film
                    found = True
                    printInfo()
                    counter += 1
        if found:
            selectSub = input ('Lütfen İstediğiniz Altyazının Numarasını Giriniz'+'('+str(saveCounter)+')(0:Hiçbiri):')
            if selectSub == "0":
                found = False
                self.subUrl = None
            elif selectSub == "":
                if saveCounter!=None:
                    self.subUrl = subTable[saveCounter-1].find("a").attrs['href']
                else:
                    found = False
                    self.subUrl = None
            else:
                self.subUrl = subTable[int(selectSub)-1].find("a").attrs['href']
                    
        return found 

    def downloadTASubs(self,dlUrl):
        url = self.subDomain + dlUrl
        urldl = self.subDomain + '/ind'
        subFileName = self.filePath + '/' + self.movieName +'.srt'
        
        r = getWeb (url,'')
        source = BeautifulSoup(r,"lxml")
        data = urllib.parse.urlencode({
                "idid": source.find("input",{"name": "idid"}).get('value'),
                "altid": source.find("input",{"name": "altid"}).get('value'),
                "sidid": source.find("input",{"name": "sidid"}).get('value')
                }).encode('ascii')
                
        r = getWeb (urldl,data)
        ziptype = r.info()["Content-Disposition"][-3:].lower()
        if ziptype=='zip':
            zipfile = ZipFile(BytesIO(r.read()))
        elif ziptype=='rar':
            zipfile = RarFile(BytesIO(r.read()))
        for fileno in zipfile.namelist():
            if fileno.lower().endswith('.srt'):
                with open(subFileName, mode='w', encoding = 'UTF-8') as f:
                    if isUTF8(zipfile.open(fileno).read()): #UTF8
                        for line in zipfile.open(fileno).readlines():
                            f.write(line.decode("UTF-8")) 
                    else: # ISO8859-9
                        for line in zipfile.open(fileno).readlines():
                            f.write(line[:-1].decode("ISO8859-9")+'\r\n')
        
        return
    
def getWeb(url,data):
    try:
        if data!='':
            req = urllib.request.urlopen(url=url,data=data)
        else:
            req = urllib.request.urlopen(url=url)
    except HTTPError as e:
        print('TASub HTTP Hatası:'+ str(e.code))
        req = ''
    except URLError as e:
        print('TASub URLError Hatası:'+ str(e.reason))
        req = ''
	#    print (req.getcode())
    return req

def isUTF8(data):
    try:
        data.decode('UTF-8')
    except UnicodeDecodeError:
        return False
    else:
        return True
   

root = sys.argv[1] #Aranacak dizin argument olarak girilir. python3 altyazi.py "/Volumes/Movies" gibi
extPattern = [".mkv",".mp4",".avi"]

print (root)
for path, subdirs, files in os.walk(root):
    for name in files:
        if name.lower().endswith(tuple(extPattern)): 
            a = MovieFile(path,name)
            if not a.findTASubs():
                print ('Altyazı bulunamadı')        
            else:
                a.downloadTASubs (a.subUrl)

            
