#v0.1
import os
import urllib.request, urllib.parse
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup # pip3 install bs4 , pip3 install lxml
import PTN #pip3 install parse-torrent-name, Windows: pip install https://github.com/divijbindlish/parse-torrent-name/archive/master.zip
from io import BytesIO
from zipfile import ZipFile
from rarfile import RarFile # pip3 install rarfile // unrar kurulu olmalı

class turkcealtyazi:

    tSubDomain = "https://www.turkcealtyazi.org"

    def __init__(self):

        return

    def solveName(self, filePath, fileName):
        parsedGroup, parsedSeason, parsedEpisode, parsedYear = "", "", "", ""
        assetFileName = os.path.splitext(fileName)[0] #Remove extension from name
        assetIsSeries = False
        parsedFile = PTN.parse(assetFileName)
        parsedAssetName = parsedFile['title']
        #print (self.assetFileName)
        if 'group' in parsedFile:
            parsedGroup = parsedFile['group'].replace("[", "").replace("]", "") #Remove [] from YTS.AM
        if 'season' in parsedFile:
            assetIsSeries = True
            parsedSeason = str(parsedFile['season']).rjust(2,'0')
            parsedEpisode = str(parsedFile['episode']).rjust(2,'0')
        if 'year' in parsedFile:
            parsedYear = parsedFile['year']
        # Add imdb page tt number here
        assetAttributes = {
            "dizi" : assetIsSeries,
            "isim" : parsedAssetName,
            "grup" : parsedGroup,
            "sezon" : parsedSeason,
            "bölüm" : parsedEpisode,
            "yıl" : str(parsedYear),
            "dosyaisim" : assetFileName,
            "dosyadizin" : filePath,
            "imdbsayfa" : ""
        }
        return assetAttributes #Returns Dictionary

    def findSubPage(self, assetName, assetYear):
        subPages = [] #list
        searchTxt = urllib.parse.quote_plus(assetName+' '+assetYear)
        r = getWeb (self.tSubDomain + '/find.php?cat=sub&find='+searchTxt,'')
        source = BeautifulSoup(r,"lxml")
        if 'arama' in source.title.string:
            subTopTable = source.find_all("div",{"style": "float:left;width:450px;"})
            for link in subTopTable:
                tmpName = link.find_all('span',{'style':'font-size:15px'})
                subPages.append({
                    "isim" : tmpName[0].get_text()+' '+tmpName[1].get_text(),
                    "sayfa" : self.tSubDomain+link.find("a").attrs['href']
                })
        else:
            for tag in source.find_all("meta"):
                if tag.get("property", None) == "og:url":
                    subPages.append({
                        "isim" : source.title.string,
                        "sayfa" : tag.get("content", None)
                    })

        return subPages # Returns List of Dictionaries, Returns [] if not found. name,webpage address

    def listSubtitles(self, assetPage):
        foundSubtitles = []
        r = getWeb (assetPage,'')
        source = BeautifulSoup(r,"lxml")
        try:
            tip = source.find("div", class_="sub-container nleft").attrs['itemtype']
        except:
            tip = ''
        if tip == '//schema.org/TVSeries':# Other one is //schema.org/Movie
            assetIsSeries = True
        else:
            assetIsSeries = False
        subTopTable = source.find("div",{"id": "altyazilar"})
        if subTopTable!=None: # If any subtitles found
            subTable = subTopTable.find_all("div",class_=None)
            del subTable[-1] #None class div 'lerden sonuncusunu sil, boş geliyor
            for link in subTable:
                aldil = link.find("div", class_="aldil").find("span").attrs['class'][0]
                aldil = aldil[-2:]
                algonderen = link.find("div", class_="algonderen").text
                datediv = link.find("div", class_="datediv").text
                alfps = link.find("div", class_="alfps").text
                ripdiv = link.find("div", class_="ripdiv").text.strip().replace(" ", "").replace("[", "").replace("]", "") #Remove [] from YTS.AM
                subWebPage = self.tSubDomain+link.find("a").attrs['href']
                if assetIsSeries: #Dizi
                    aa = link.find("div", class_="alcd").text.strip().replace("\n", "").replace("|", "")
                    sezon = aa[1:3]
                    bolum = aa[-2:]
                    alcd = ""
                else: #Movie
                    alcd = link.find("div", class_="alcd").text.strip().replace("\n", "").replace("|", "")
                    sezon = ""
                    bolum = ""
                foundSubtitles.append ({
                    "dizi" : assetIsSeries,
                    "dil" : aldil,
                    "gönderen" : algonderen,
                    "tarih" : datediv,
                    "fps" : alfps,
                    "grup" : ripdiv,
                    "sezon": sezon,
                    "bölüm" : bolum,
                    "sayfa" : subWebPage
                })

        return foundSubtitles # Returns List of Dictionaries, Returns [] if not found.

    def downloadSub(self, assetPage):
        urldl = self.tSubDomain + '/ind'
        subFile = ''
        r = getWeb (assetPage,'')
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

                if isUTF8(zipfile.open(fileno).read()): #UTF8
                    for line in zipfile.open(fileno).readlines():
                        subFile = subFile + line.decode("UTF-8")
                else: # ISO8859-9
                    for line in zipfile.open(fileno).readlines():
                        subFile = subFile + line[:-1].decode("ISO8859-9")+'\n' # Windows style line ends

        return subFile # Returns .srt file as string

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