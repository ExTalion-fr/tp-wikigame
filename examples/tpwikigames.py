from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os

listElements = ["Modifier", "Wikipédia:", "Aide:", "modifier les données", "Spécial:", "Portail:", "Projet:", "d:", "API ", "Fichier:"]
tour: int
iStart: int
nb: int
arrayChoix: dict
soupStart: BeautifulSoup
soupEnd: BeautifulSoup
soup: BeautifulSoup

def sendRequest():
    req = Request(
        url="https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    soupRequest = BeautifulSoup(webpage, 'html.parser')
    if soupRequest and soupRequest.find('span', attrs={"class": "mw-page-title-main"}) and type(soupRequest) is BeautifulSoup:
        return soupRequest
    else:
        sendRequest()

def startTour():
    os.system('cls')
    global tour
    global iStart
    global nb
    global soupStart
    global soupEnd
    global soup
    global arrayChoix
    arrayChoix = {}
    print("************************ WikiGames **** tour " + str(tour))
    print("Départ: " + soupStart.find('span', attrs={"class": "mw-page-title-main"}).text)
    print("Arrivée: " + soupEnd.find('span', attrs={"class": "mw-page-title-main"}).text)
    print("Actuellement: " + soup.find('span', attrs={"class": "mw-page-title-main"}).text)
    i = 1
    nb = 0
    for reponse in soup.find_all('a'):
        if reponse.find_parents('div', attrs={"class": "mw-parser-output"}) and reponse.find_parent('p'):
            if 'title' in reponse.attrs and not 'class' in reponse.attrs:
                title = reponse.attrs['title']
                arrayChoix[i] = { 'title': title, 'href': reponse.attrs['href'] }
                for element in listElements:
                    if title.startswith(element):
                        title = None
                        break
                if title:
                    nb += 1
                    if i < iStart:
                        i += 1
                        continue
                    elif i >= iStart + 20:
                        continue
                    if i < 10:
                        print("0" + str(i) + " - " + title)
                    else:
                        print(str(i) + " - " + title)
                    i += 1
    if iStart > 20:
        print("98 - Voir les précédentes")
    if nb > 20:
        print("99 - Voir la suite")
    checkAnswer()

def checkAnswer():
    global nb
    global arrayChoix
    global iStart
    global tour
    global soup
    choix = int(input("Votre choix: "))
    if choix >= 1 and choix <= 20:
        if choix in arrayChoix:
            tour += 1
            req = Request(
                url="https://fr.wikipedia.org" + arrayChoix[choix]['href'],
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            soup = BeautifulSoup(urlopen(req).read(), 'html.parser')
            startTour()
        else:
            print("Choix invalide")
            checkAnswer()
    elif choix == 99 and nb > 20:
        iStart += 20
        startTour()
    elif choix == 98 and iStart > 20:
        iStart -= 20
        startTour()
    else:
        print("Choix invalide")
        checkAnswer()

def startGame():
    global tour
    global iStart
    global soupStart
    global soupEnd
    global soup
    tour = 1
    iStart = 1
    soupStart = sendRequest()
    soupEnd = sendRequest()
    soup = soupStart
    startTour()

startGame()