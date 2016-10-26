import requests

def zapisi_vsebino():
    #osnovni naslov : http://home.izum.si/cobiss/top_gradivo/
    vsebina = []
    for i in range(2,15): #šteje po letih
        for j in range(1,12): #šteje po mesecih
    a = requests.get('http://home.izum.si/cobiss/top_gradivo/default.asp?l=20'+'{num:02d}'.format(num=i)+'&m='+'{num:02d}'.format(num=j)+'&tipg=m%25&Submit=IZDELAJ+SEZNAM', auth=('user', 'pass'))
    vsebina.append(a.text)
    return (vsebina)


#a = requests.get('http://home.izum.si/cobiss/top_gradivo/default.asp?l=2003&m=04&tipg=m%25&Submit=IZDELAJ+SEZNAM')
# print (a.text)
#'http://home.izum.si/cobiss/top_gradivo/default.asp?l=20'+'{num:02d}'.format(num=i)+'&m='+'{num:02d}'.format(num=i)+'&tipg=m%25&Submit=IZDELAJ+SEZNAM'


print(zapisi_vsebino())