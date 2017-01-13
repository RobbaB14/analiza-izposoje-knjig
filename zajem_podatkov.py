import re
import csv
import requests
from os import listdir
from os.path import isfile, join


def zapisi_vsebino():
    #vsebino vseh spletnih strani shrani v slovar s ključi (l,m)
    vsebina = {}
    for l in range(2,17): #šteje po letih
        if l<=15:
            for m in range(1, 13): #šteje po mesecih
                a = requests.get('http://home.izum.si/cobiss/top_gradivo/default.asp?l=20' + str(l).zfill(2)+'&m=' + str(m).zfill(2) + '&tipg=m%25&Submit=IZDELAJ+SEZNAM', auth=('user', 'pass'))
                vsebina[(l,m)] = a.text
        else: #za leto 2016 imamo podatke samo do vključno septembra
            for m in range(1, 10):  # šteje po mesecih
                a = requests.get(
                    'http://home.izum.si/cobiss/top_gradivo/default.asp?l=20' + str(l).zfill(2) + '&m=' + str(m).zfill(2) + '&tipg=m%25&Submit=IZDELAJ+SEZNAM', auth=('user', 'pass'))
                vsebina[(l,m)] = a.text
    return vsebina


def shrani_vsebino(imenik):
    for k in imenik.keys():
        a = open('leto20{}mesec{}.txt'.format(str(k[0]).zfill(2), k[1]), 'w', encoding='utf-8')
        a.write(imenik[k])
        a.close()



regex_dela = re.compile(
    r"<tr><FORM NAME='Id-ji' METHOD='POST' ACTION='cobiss-si-id\.asp'><td align=right class='small\d*?'>\d*?\.</td>.*?"
    r"<td align=left class='small\d*?'>(?P<naslov>.*?)</td>.*?"
    r"<td align=left class='small\d*?'>(?P<avtor>.*?)</td>.*?"
    r"<td align=right class='small\d*?'>(?P<izposoja>\d*?)&nbsp;</td>.*?"
    r"<td align=right class='small\d?'>(?P<rezervacija>\d*?)&nbsp;</td>"
    ,flags=re.DOTALL
    )

def pocisti_delo(delo):
    podatki = delo.groupdict()
    podatki['naslov'] = podatki['naslov']
    podatki['avtor'] = podatki['avtor']
    podatki['izposoja'] = int(podatki['izposoja'])
    podatki['rezervacija'] = int(podatki['rezervacija'])
    # ker avtorji v podatkih, ki jih zajemamo niso dosledno zapisani z malimi črkami z veliko začetnico, to popravimo
    z = podatki['avtor'].split(' ')
    z[0] = z[0].capitalize()
    a = ''
    for i in z:
        a += i + ' '
    podatki['avtor'] = a
    return podatki



def beri(ime_datoteke):
    a = open(ime_datoteke, 'r', encoding='utf-8')
    b = a.read()
    a.close()
    return b


# ker bo analiza podatkov lažja, če vse podatke združimo v eno tabelo, to tudi naredimo:
def enotni_csv():
    txt_files = [f for f in listdir('.\\') if isfile(join('.\\', f)) and f[-4:]=='.txt']
    with open('podatki.csv', 'w', encoding='utf-8') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=['naslov', 'avtor', 'izposoja', 'rezervacija', 'leto', 'mesec'])
        writer.writeheader()
        for f in txt_files:
            vsebina = beri(f)
            podatki = re.finditer(regex_dela, vsebina)
            slovarji = []
            leto = f[4:8]
            mesec = f[13:-4]
            for a in podatki:
                b = pocisti_delo(a)
                b['leto'] = leto
                b['mesec']= mesec
                slovarji.append(b)
            for slovar in slovarji:
                writer.writerow(slovar)

#naredimo .txt file z vsebino strani
vsebina = zapisi_vsebino()
shrani_vsebino(vsebina)

#naredimo csv s tabelo z vsemi podatki
enotni_csv ()