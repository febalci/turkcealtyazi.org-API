# turkcealtyazi.org script
Film ve diziler için turkcealtyazi.org altyazı indirme Python API (Python3)

# Kurulum:
Beautifulsoap, parse-torrent-name ve rarfile modülleri kurulu olmalıdır. Ayrıca sistemde unrar kurulu olmalıdır:

```pip3 install bs4```

```pip3 install lxml```

```pip3 install rarfile```

```pip3 install parse-torrent-name```

Windows altında çalıştırıyorsanız pip3 install parse-torrent-name hata verecektir. O halde şu komutla parse-torrent-name kurabilirsiniz:

```pip3 install https://github.com/divijbindlish/parse-torrent-name/archive/master.zip```

# Kullanım:
Script Dizininde bulunan altyazi.py API versiyonu değildir. Tek başına çalıştırmak içindir.

```python3 altyazi.py "/Volumes/movies"```

veya (Windows'da \ yerine / kullanın)

```python3 altyazi.py "C:/Users/Aa Bb/Movies"```

Sample Dizininde bulunan test.py, api kullanımına örnek olarak bulunmaktadır.
```python3 test.py "/Volumes/movies"```

# API Kullanımı:
### solvename(dosyadizini,dosyaadı)
İndirilen torrent dizi/film dosyasının isminde yer alan bilgilerden dizi/film hakkında bilgi edinir.  
solvename['dizi'] : Boolean  
&nbsp;&nbsp;Eğer dosya dizi dosyası ise 'True', film dosyası ise 'Movie' alır.  
solvename['isim'] : String  
&nbsp;&nbsp;Dizi ya da Filmin ismi  
solvename['grup'] :  
&nbsp;&nbsp;Dosyayı rip yapan grubun ismi  
solvename['sezon'] :  
&nbsp;&nbsp;Eğer dizi ise sezonu yer alır, film ise boştur.  
solvename['bölüm'] :  
&nbsp;&nbsp;Eğer dizi ise bölümü yer alır, film ise boştur.  
solvename['yıl'] :  
&nbsp;&nbsp;Dizi/Film'in çekildiği yıl  
solvename['dosyaismi'] :  
&nbsp;&nbsp;Dosyanın ismi yer alır  
solvename['dosyadizin'] :  
&nbsp;&nbsp;Dosyanın dizini yer alır  
solvename['imdbsayfa'] :  
&nbsp;&nbsp;Henüz kullanılmamaktadır  

### findSubPage(isim, Yıl)
Dizi/Film için turkcealtyazi.org'da ilgili sayfayı bulur. Aramada birden fazla sayfa gelirse list oluşturur.  
findSubPage[i]['isim'] :  
&nbsp;&nbsp;Dizi/Film'in adı yer alır  
findSubPage[i]['sayfa'] :  
&nbsp;&nbsp;İlgili web sayfasının adresidir  

### listSubtitles(websayfası)
Verilen turkcealtyazi.org Dizi/Film bilgi sayfası içinden tüm altyazı bilgilerini getirir. Aramada birden fazla sayfa gelirse list oluşturur.  
listSubtitles[i]['dizi'] :  
&nbsp;&nbsp;Eğer altyazi dizi dosyası ise 'True', film dosyası ise 'Movie' alır.  
listSubtitles[i]['dil'] :  
&nbsp;&nbsp;Altyazının dili. Türkçe için 'tr', İngilizce için 'en'  
listSubtitles[i]['gönderen'] :  
&nbsp;&nbsp;Altyazıyı gönderen çevirmenin ismi  
listSubtitles[i]['tarih'] :  
&nbsp;&nbsp;Altyazının gönderilme tarihi  
listSubtitles[i]['fps'] :  
&nbsp;&nbsp;Altyazının uyumlu olduğu fps  
listSubtitles[i]['grup'] :  
&nbsp;&nbsp;Altyazının uyumlu olduğu rip grubu  
listSubtitles[i]['sezon'] :  
&nbsp;&nbsp;Altyazının ilgili dizi sezonu  
listSubtitles[i]['bölüm'] :  
&nbsp;&nbsp;Altyazının ilgili dizi bölümü  
listSubtitles[i]['sayfa'] :  
&nbsp;&nbsp;Altyazının bulunduğu turkcealtyazi.org web sayfası  

### downloadSub(websayfası)
Altyazının turkcealtyazi.org web sayfasından dosyayı indirir. Zip veya Rar dosyasını açıp, .srt dosyasının UTF8'e çevirerek string olarak alır.
