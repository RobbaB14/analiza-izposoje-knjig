import requests

def zapisi_vsebino():
    #osnovni naslov : http://home.izum.si/cobiss/top_gradivo/
    vsebina = []
    for i in range(2,16): #šteje po letih
        if i<=15:
            for j in range(1,12): #šteje po mesecih
            a = requests.get('http://home.izum.si/cobiss/top_gradivo/default.asp?l=20'+str(j).zfill(2)+'&m='+str(i).zfill(2)+'&tipg=m%25&Submit=IZDELAJ+SEZNAM', auth=('user', 'pass'))
            vsebina.append(a.text)
        else: #za leto 2016 imamo podatke samo do vlkjučno septembra
            for j in range(1, 9):  # šteje po mesecih
                a = requests.get(
                    'http://home.izum.si/cobiss/top_gradivo/default.asp?l=20' + 'str(j).zfill(2)' + '&m=' + 'str(i).zfill(2)' + '&tipg=m%25&Submit=IZDELAJ+SEZNAM', auth=('user', 'pass'))
                vsebina.append(a.text)
    return (vsebina)


print(zapisi_vsebino())



