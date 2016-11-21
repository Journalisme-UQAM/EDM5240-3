# coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup 

url = "http://www.contracts-contrats.hc-sc.gc.ca/cfob/mssid/contractdisc.nsf/WEBbypurposeF?OpenView&RP=2016-2017~1&Count=3000&lang=fra&"

fichier = "sante-contrats-JHR.csv"

entetes = {
    "User-Agent":"Sarah Daoust-Braun pour amasser des données pour le cours EDM5240 à l'UQAM",
    "From":"sarahdaoustbraun@gmail.com"
}

contenu = requests.get(url, headers=entetes) 
page = BeautifulSoup(contenu.text, "html.parser") 
# print(page)

i = 0

table = []

for ligne in page.find_all('tr'):
    if i != 0:
        # print(ligne.contents[0].string)
        contrat = {
            'URL':'http://www.contracts-contrats.hc-sc.gc.ca/' + ligne.contents[2].a.get('href'), # J'ai ajouté cette ligne. C'est vraiment la seule chose qui manque à ton moissonnage: l'URL de la page de chaque page. C'est pratique pour faire des vérifications ultérieurement dans nos données
            'date':ligne.contents[0].string, 
            'fournisseur':ligne.contents[2].string,
            'description':ligne.contents[4].string
        }
        
        hyperlien = requests.get('http://www.contracts-contrats.hc-sc.gc.ca/' + ligne.contents[2].a.get('href'), headers=entetes) 
        souspage = BeautifulSoup(hyperlien.text, "html.parser")
        toutP = souspage.find_all('p')
        print(len(toutP))
        
        contrat['reference'] = toutP[4].text
        contrat['periode'] = toutP[7].text
        contrat['methode invitation'] = toutP[8].text
        contrat['marches pluriannuels'] = toutP[9].text
        contrat['type document'] = toutP[10].text
        contrat['modifications'] = toutP[11].text
        contrat['valeur originale'] = toutP[12].text
        contrat['valeur cumulative'] = toutP[13].text
        contrat['valeur globale'] = toutP[14].text
        contrat['commentaires'] = toutP[15].text
        
        print(contrat)
        
        table.append(contrat)
        
    i = i+1
# Dans un des scripts que je vous ai envoyés, j'ai fait une erreur.
# Quand on écrit « =+1 », on dit «la variable est égale à (plus) 1».
# C'est « +=1 » qu'il faut écrire pour augmenter de 1 la valeur d'une variable dans une boucle. Tu as su contourner cette erreur de ma part!

f1 = open(fichier, 'w')
document = csv.DictWriter(f1,['URL', 'date', 'fournisseur', 'description', 'reference', 'periode', 'methode invitation', 'marches pluriannuels', 'type document', 'modifications', 'valeur originale', 'valeur cumulative', 'valeur globale', 'commentaires']) # J'ai ajouté l'entête de la colonne des URL
document.writeheader()

for contrat in table:
    document.writerow(contrat)

# Excellent script!
# Il y a deux choses que j'aime beaucoup:
# 1. Que tu sois allée chercher d'autres commandes dans la documentation de BeautifulSoup
# 2. Que tu aies utilisé une autre approche, une autre façon de moissonner les données, par le biais d'un dictionnaire.
# Et ça fonctionne! Bravo!