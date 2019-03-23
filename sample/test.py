from turkcealtyazi_api import turkcealtyazi
import sys,os

root = sys.argv[1] #Aranacak dizin argument olarak girilir. python3 altyazi.py "/Volumes/Movies" gibi
extPattern = [".mkv",".mp4",".avi"]

tamovie = turkcealtyazi()
for path, subdirs, files in os.walk(root):
    for name in files:
        if name.lower().endswith(tuple(extPattern)):
# Dizi/Film İsmini Çözümle ve Kullanıcıya Doğrulat
            solvedFile = tamovie.solveName(path,name)
            print (name)
            match = input (solvedFile['isim']+'?')
            if match == "":
                aramaIsim = solvedFile['isim']
                aramaYil = solvedFile['yıl']
            else:
                aramaIsim = match
                aramaYil = ""

# Dizi/Film Sayfasını Bul, Birden Fazla İlişkili Sayfa Gelirse Kullanıcıya Seçtir
            subPage = tamovie.findSubPage(aramaIsim,aramaYil)
            if len(subPage)== 0:
                print ('Film/Dizi Bulunamadı...')    
            elif len(subPage)== 1:
                subPageUrl = subPage[0]['sayfa']
            elif len(subPage) > 1:
                counter = 1
                for pageItem in subPage:
                    print ("%2s" % counter +"."+pageItem['isim'])
                    counter += 1
                match = input ('Lütfen Doğru Film/Dizinin Numarasını Giriniz (1):')
                if match == "":
                    subPageUrl = subPage[0]['sayfa']
                else:
                    subPageUrl = subPage[int(match)-1]['sayfa']

# Dizi/Film Altyazılarını Listele ve Kullanıcı seçim yapsın
            subList = tamovie.listSubtitles(subPageUrl)
            if len(subList)== 0:
                print ('Bu Film/Dizi İçin Altyazı Bulunamadı...')
            else:
                counter = 1
                for subItem in subList:
                    satir = subItem['dil'].upper()+' '+subItem['sezon']+' '+subItem['bölüm']+' '+subItem['tarih']+' '+subItem['grup']
                    print ("%2s" % counter +"."+satir)
                    counter += 1
                match = input ('Lütfen İstediğiniz Altyazının Numarasını Giriniz (0:Hiçbiri):')
                print (match)
                if match != '0' and match!= '':
                    subDlUrl = subList[int(match)-1]['sayfa']
                    print (tamovie.downloadSub(subDlUrl))
            
              