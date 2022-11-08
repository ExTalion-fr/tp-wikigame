
from __future__ import print_function, unicode_literals

import sys
from pprint import pprint
from PyInquirer import prompt, Separator
from examples import custom_style_2
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
questions = [
    {
        'type': 'list',
        'name': 'theme',
        'message': 'Choisissez une page',
        'choices': []
    },
]

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

def gameWin():
    print("******************************************************************")
    print("************************ Vous avez gagner ************************")
    print("******************************************************************")

def startTour():
    # sys.stdout.write('\x1b[1J')
    os.system('cls')
    global tour
    global iStart
    global nb
    global soupStart
    global soupEnd
    global soup
    global arrayChoix
    global questions
    arrayChoix = {}
    questions[0]['choices'] = []
    if soupEnd.find('span', attrs={"class": "mw-page-title-main"}).text == soup.find('span', attrs={"class": "mw-page-title-main"}).text:
        gameWin()
        return
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
                        questions[0]['choices'].append("0" + str(i) + " - " + title)
                        # print("0" + str(i) + " - " + title)
                    else:
                        questions[0]['choices'].append(str(i) + " - " + title)
                        # print(str(i) + " - " + title)
                    i += 1
    questions[0]['choices'].append(Separator())
    if iStart > 20:
        questions[0]['choices'].append("98 - Page précédente")
        # print("98 - Voir les précédentes")
    if nb > 20:
        questions[0]['choices'].append("99 - Page suivante")
        # print("99 - Voir la suite")
    checkAnswer()

def checkAnswer():
    global nb
    global arrayChoix
    global iStart
    global tour
    global soup
    global questions
    choix = prompt.prompt(questions, style=custom_style_2)
    choix = int(choix['theme'][0:2])
    # choix = int(input("Votre choix: "))
    if choix == 99 and nb > 20:
        iStart += 20
        startTour()
    elif choix == 98 and iStart > 20:
        iStart -= 20
        startTour()
    else:
        tour += 1
        req = Request(
            url="https://fr.wikipedia.org" + arrayChoix[choix]['href'],
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        soup = BeautifulSoup(urlopen(req).read(), 'html.parser')
        startTour()

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

# questions = [
#     {
#         'type': 'list',
#         'name': 'theme',
#         'message': 'What do you want to do?',
#         'choices': [
#             'Order a pizza',
#             'Make a reservation',
#             Separator(),
#             'Ask for opening hours',
#             {
#                 'name': 'Contact support',
#                 'disabled': 'Unavailable at this time'
#             },
#             'Talk to the receptionist'
#         ]
#     },
# ]



# answers = prompt.prompt(questions, style=custom_style_2)
# pprint(answers)
