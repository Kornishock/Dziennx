from flask import Flask, request, render_template

from bs4 import BeautifulSoup
import requests


app = Flask(__name__)

def doInt(data):
    return int(data[0:2] + data[3:5] + data[6:])


class Ocena():
    def __init__(self, przedmiot, ocena, opis, waga, data, nauczyciel, ):
        self.przedmiot=przedmiot
        self.ocena=ocena
        self.opis=opis
        self.waga=waga
        self.data=data[3:5]+"-"+data[0:2]+"-"+data[6:]
        self.nauczyciel=nauczyciel
        self.intData=doInt(data)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def wczytajTabele(tabela):
    print(tabela)
    wszystkieoceny=[]
    ocenyDoDodania=[]
    for tr in tabela.tbody.find_all('tr'):  # wszystkie tr w tabeli
        licznikTd = 1  # informuje w której kolumnie tabeli jesteśmy
        czyPusty = 0  # 1 jeśli kolumna nie zawiera oceny

        przedmiot = 0
        ocena = 0.00
        opis = 0
        waga = 0
        data = 0
        nauczyciel = 0

        for td in tr.find_all('td'):
            if licznikTd == 1:
                przedmiot = td.text

            if licznikTd == 2:
                if td.span != None:
                    if td.span.text[1:] == "-":
                        ocena = float(td.span.text[0]) - 0.25

                    elif td.span.text[1:] == "+":
                        ocena = float(td.span.text[0]) + 0.5

                    elif is_number(td.span.text[0]) != 1:
                        czyPusty = 1
                        break

                    else:
                        ocena = float(td.span.text[0])

                else:
                    czyPusty = 1
                    break

            if licznikTd == 3:
                opis = td.text

            if licznikTd == 4 and len(td.text) > 0:
                waga = int(td.text[0])

            if licznikTd == 5 and len(td.text) > 0:
                data = td.text

            if licznikTd == 6 and len(td.text[0]) > 0:
                nauczyciel = td.text

            licznikTd += 1

        if czyPusty == 0:  # wypisuje dane wczytanego wiersza tabeli, zawierającego ocenę
            wszystkieoceny.append(Ocena(przedmiot, ocena, opis, waga, data, nauczyciel))
            ocenyDoDodania.append((przedmiot, ocena, opis, waga, nauczyciel, data) )

    return wszystkieoceny

def wczytajOceny(login, password):
    data = {}

    with requests.Session() as s:

        page = s.get(
            'https://adfslight.resman.pl/LoginPage.aspx?ReturnUrl=%2f%3fwa%3dwsignin1.0%26wtrealm%3dhttps%253a%252f%252fcufs.resman.pl%253a443%252frzeszow%252fAccount%252fLogOn%26wctx%3drm%253d0%2526id%253dADFS%2526ru%253d%25252frzeszow%25252fFS%25252fLS%25253fwa%25253dwsignin1.0%252526wtrealm%25253dhttps%2525253a%2525252f%2525252fuonetplus.resman.pl%2525252frzeszow%2525252fLoginEndpoint.aspx%252526wctx%25253dhttps%2525253a%2525252f%2525252fuonetplus.resman.pl%2525252frzeszow%2525252fLoginEndpoint.aspx%26wct%3d2018-02-04T18%253a08%253a18Z&wa=wsignin1.0&wtrealm=https%3a%2f%2fcufs.resman.pl%3a443%2frzeszow%2fAccount%2fLogOn&wctx=rm%3d0%26id%3dADFS%26ru%3d%252frzeszow%252fFS%252fLS%253fwa%253dwsignin1.0%2526wtrealm%253dhttps%25253a%25252f%25252fuonetplus.resman.pl%25252frzeszow%25252fLoginEndpoint.aspx%2526wctx%253dhttps%25253a%25252f%25252fuonetplus.resman.pl%25252frzeszow%25252fLoginEndpoint.aspx&wct=2018-02-04T18%3a08%3a18Z').content

        data["Username"] = login
        data["Password"] = password
        data["x"] = "49"
        data["y"] = "1"

        # https://adfslight.resman.pl/LoginPage.aspx?ReturnUrl=%2f%3fwa%3dwsignin1.0%26wtrealm%3dhttps%253a%252f%252fcufs.resman.pl%253a443%252frzeszow%252fAccount%252fLogOn%26wctx%3drm%253d0%2526id%253dADFS%2526ru%253d%25252frzeszow%25252fFS%25252fLS%25253fwa%25253dwsignin1.0%252526wtrealm%25253dhttps%2525253a%2525252f%2525252fuonetplus.resman.pl%2525252frzeszow%2525252fLoginEndpoint.aspx%252526wctx%25253dhttps%2525253a%2525252f%2525252fuonetplus.resman.pl%2525252frzeszow%2525252fLoginEndpoint.aspx%26wct%3d2018-03-04T13%253a39%253a48Z

        s.post(
            'https://adfslight.resman.pl/LoginPage.aspx',
            data=data)
        open_page = s.get(
            "https://adfslight.resman.pl/?wa=wsignin1.0&wtrealm=https%3a%2f%2fcufs.resman.pl%3a443%2frzeszow%2fAccount%2fLogOn&wctx=rm%3d0%26id%3dADFS%26ru%3d%252frzeszow%252fFS%252fLS%253fwa%253dwsignin1.0%2526wtrealm%253dhttps%25253a%25252f%25252fuonetplus.resman.pl%25252frzeszow%25252fLoginEndpoint.aspx%2526wctx%253dhttps%25253a%25252f%25252fuonetplus.resman.pl%25252frzeszow%25252fLoginEndpoint.aspx&wct=2018-03-04T14%3a13%3a15Z")
        soup = BeautifulSoup(open_page.text, "lxml")

        # print(soup.prettify())

        wa = soup.find('input', {'name': 'wa'}).get('value')
        wresult = soup.find('input', {'name': 'wresult'}).get('value')
        wctx = soup.find('input', {'name': 'wctx'}).get('value')

        data2 = {}
        data2["wa"] = wa
        data2["wresult"] = wresult
        data2["wctx"] = wctx

        s.post('https://cufs.resman.pl/rzeszow/Account/LogOn', data=data2)

        open_page = s.get(
            "https://cufs.resman.pl/rzeszow/FS/LS?wa=wsignin1.0&wtrealm=https%3a%2f%2fuonetplus.resman.pl%2frzeszow%2fLoginEndpoint.aspx&wctx=https%3a%2f%2fuonetplus.resman.pl%2frzeszow%2fLoginEndpoint.aspx")

        #########
        wa = soup.find('input', {'name': 'wa'}).get('value')
        wresult = soup.find('input', {'name': 'wresult'}).get('value')
        wctx = soup.find('input', {'name': 'wctx'}).get('value')

        data3 = {}
        data3["wa"] = wa
        data3["wresult"] = wresult
        data3["wctx"] = wctx

        print(data2)
        print(data3)

        s.post('https://uonetplus.resman.pl/rzeszow/LoginEndpoint.aspx', data=data3)

        oceny = []

        s.get("https://uonetplus-opiekun.resman.pl/rzeszow/02lo/Start/Index")
        open_page = s.get("https://uonetplus-opiekun.resman.pl/rzeszow/02lo/Oceny.mvc/Wszystkie?details=2&okres=24344")
        soup = BeautifulSoup(open_page.text, "lxml")
        tabela = soup.find('table', class_="ocenySzczegoly-table")
        print(soup.prettify())
        print(tabela)
        for i in wczytajTabele(tabela):
            oceny.append(i)

        s.get("https://uonetplus-opiekun.resman.pl/rzeszow/02lo/Start/Index")
        open_page = s.get(
            "https://uonetplus-opiekun.resman.pl/rzeszow/02lo/Oceny.mvc/Wszystkie?details=2&okres=24345")
        soup = BeautifulSoup(open_page.text, "lxml")
        tabela = soup.find('table', class_="ocenySzczegoly-table")
        print(soup.prettify())
        print(tabela)
        for i in wczytajTabele(tabela):
            oceny.append(i)



    return oceny

def znajdzPrzedmioty(tabela): #zwraca listę nazw wszystkiech przedmiotów

    przedmioty=[]

    for i in tabela:
        if (i.przedmiot in przedmioty)==0:
            przedmioty.append(i.przedmiot)

    return przedmioty


def wybierzPrzedmiot(przedmiot, tabela): # zwraca oceny z danego przedmiotu
    zwracanaTabela=[]
    for i in tabela:
        if i.przedmiot == przedmiot:
            zwracanaTabela.append(i)

    return zwracanaTabela

def liczPostep(przedmiot, tabela): #zwraca tabelę, gdzie w [0][n] umieszczone są daty, a w [1][n] średnie z danego przedmiotu w tych datach
    suma = 0
    sumaWag = 0
    zwracanaTabela = [[],[],[]]
    tab=wybierzPrzedmiot(przedmiot, tabela)
    licznikDat=-1
    for i in tab:
        suma += float(i.ocena)*float(i.waga)
        sumaWag += float(i.waga)
        if (i.data in zwracanaTabela[0])==0:
            licznikDat+=1
            zwracanaTabela[0].append(i.data)
            zwracanaTabela[1].append(round(suma / sumaWag, 3))
            zwracanaTabela[2].append([])
            zwracanaTabela[2][licznikDat].append(i)

        else:
            zwracanaTabela[1][licznikDat] = round(suma / sumaWag, 3)
            zwracanaTabela[2][licznikDat].append(i)



    return zwracanaTabela


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('logowanie.html', loginerror="")

    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']

        try:
            tabelaOcen= wczytajOceny(login,password)
        except:
            return render_template('logowanie.html', loginerror="Niepoprawny login lub hasło.")

        liczPostep("Matematyka", tabelaOcen)


        #
        ocenyStr=[]

        for i in tabelaOcen:
            ocenyStr.append([i.data, str(i.intData), i.przedmiot, i.nauczyciel, str(i.ocena),i.opis])
        #

        wszystkieTabelePostepu=[]

        for i in znajdzPrzedmioty(tabelaOcen):
            wszystkieTabelePostepu.append(liczPostep(i, tabelaOcen))

        print(wszystkieTabelePostepu)

        return render_template('panel.html', content=wszystkieTabelePostepu, przedmioty=znajdzPrzedmioty(tabelaOcen))



if __name__ == "__main__":
    app.run(debug=True)