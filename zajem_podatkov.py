import re
import csv
import requests


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
    return podatki


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    with open(ime_datoteke, 'w') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames= imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

def beri(ime_datoteke):
    a = open(ime_datoteke, 'r', encoding='utf-8')
    b = a.read()
    a.close()
    return b


def zapisi_csv(ime_txt_datoteke, ime_csv_datoteke):
    #vzame vsebino prve datoteke, poišče podatke in oblikuje tabelo, ki jo shrani v csv datoteko
    vsebina = beri(ime_txt_datoteke)
    podatki = re.finditer(regex_dela, vsebina)
    slovarji = []
    for a in podatki:
        slovarji.append(pocisti_delo(a))
    with open(ime_csv_datoteke, 'w', encoding = 'utf-8') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=['naslov', 'avtor', 'izposoja', 'rezervacija'])
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

#naredimo .txt file z vsebino strani
vsebina = zapisi_vsebino()
shrani_vsebino(vsebina)

#naredimo tabele
for l in range(2, 17):  # šteje po letih
    if l <= 15:
        for m in range(1, 13):  # šteje po mesecih
            zapisi_csv('leto20{}mesec{}.txt'.format(str(l).zfill(2),m), 'leto20{}mesec{}.csv'.format(str(l).zfill(2),m))

    else:  # za leto 2016 imamo podatke samo do vključno septembra
        for m in range(1, 10):  # šteje po mesecih
            zapisi_csv('leto20{}mesec{}.txt'.format(str(l).zfill(2), m), 'leto20{}mesec{}.csv'.format(str(l).zfill(2),m))
