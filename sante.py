# coding: utf-8

#AVANT DE LANCER LE SCRIPT, IL FAUT CRÉER UN ENVIRONNEMENT VIRUTEL (virtualenv -p /usr/bin/python3 py3env) ET L'ACTIVER DANS LE TERMINAL (source py3env/bin/activate)
#IL FAUT AUSSI IMPORTER LES MODULES requests (sudo pip install requests) ET BeautifulSoup (sudo pip install BeautifulSoup4)
#APRÈS CES ÉTAPES, ON PEUT LANCER LE SCRIPT CI-DESSOUS

import csv
import requests
from bs4 import BeautifulSoup 


url = "http://www.contracts-contrats.hc-sc.gc.ca/cfob/mssid/contractdisc.nsf/WEBbypurposeF?OpenView&RP=2016-2017~1&Count=3000&lang=fra&"
#JE VEUX ALLER MOISSONNER DES DONNÉES DU SITE GOUVERNEMENTAL SANTÉ CANADA. CETTE PAGE CONTIENT LA LISTE DE CONTRATS CONCLUS ENTRE SANTÉ CANADA ET SES FOURNISSEURS POUR LE PREMIER TRIMESTRE 2016-2017

fichier = "sante-contrats.csv"
#MES DONNÉES SERONT PLACÉES DANS CE FICHIER CSV 

entetes = {
    "User-Agent":"Sarah Daoust-Braun pour amasser des données pour le cours EDM5240 à l'UQAM",
    "From":"sarahdaoustbraun@gmail.com"
}


contenu = requests.get(url, headers=entetes) 
#JE DEMANDE À requests D'ÉTABLIR UNE CONNEXION AVEC MON URL
page = BeautifulSoup(contenu.text, "html.parser") 
#BEAUTIFULSOUP VA ANALYSER LE TEXTE DE CETTE PAGE 
print(page)

i = 0
#ON CRÉE UN COMPTEUR 

table = []
#ON CRÉE UN TABLEAU POUR CONTENIR LES LIGNES DU TABLEAU DE LA PAGE WEB

for ligne in page.find_all('tr'):
    if i != 0:
    #IL FAUT QUE LE COMPTEUR SOIT DIFFÉRENT DE LA VALEUR 0 PARCE QU'ON NE VEUT PAS LA PREMIÈRE LIGNE DU TABLEAU QUI EST L'ENTÊTE
    
        print(ligne.contents[0].string)
        #JE FAIS DES TESTS. CETTE LIGNE DE CODE ME PERMET D'AFFICHER LES DATES DE TOUS LES CONTRATS, DONC LES INFOS DE LA PREMIÈRE COLONNE DE LA PAGE WEB
        #.CONTENTS PERMET D'ACCÉDER AUX DIFFÉRENTS ÉLÉMENTS (CHILDREN) DE CHAQUE LIGNE DANS LE CODE HTML DE LA PAGE WEB
        #.STRING PERMET D'ALLER CHERCHER LE TEXTE ENTRE LES BALISES 
        
        #APRÈS AVOIR OBSERVÉ LE CODE SOURCE DE LA PAGE WEB, ON REMARQUE QU'IL Y A BIZARREMENT DES ESPACES VIDES (, ,) ENTRE LES BALISES <tr> DE CHAQUE LIGNE DU TABLEAU
        #MOI JE VEUX LES INFOS ENTRE CERTAINES BALISES <td>
        #JE VEUX LES INFOS DE LA PREMIÈRE BALISE <td> [0], LA TROISIÈME [2], LA CINQUIÈME [4] 
        contrat = {
            'date':ligne.contents[0].string, 
            'fournisseur':ligne.contents[2].string,
            'description':ligne.contents[4].string
        }
        #J'AI CRÉÉ UN DICTIONNAIRE QUI VA ALLER CHERCHER LES INFOS Du TABLEAU DE LA PAGE WEB
        
        hyperlien = requests.get('http://www.contracts-contrats.hc-sc.gc.ca/' + ligne.contents[2].a.get('href'), headers=entetes) 
        souspage = BeautifulSoup(hyperlien.text, "html.parser")
        toutP = souspage.find_all('p')
        #ICI, JE VAIS CHERCHER LES INFOS DÉTAILLÉES DE CHAQUE CONTRAT CONTENUES DANS LES HYPERLIENS DE LA COLONNE "Fournisseur"
        #QUAND JE REGARDE LE CODE SOURCE DES PAGES DE CONTRAT DÉTAILLÉ, JE REMARQUE QUE LES INFOS QUE JE VEUX SONT ENTRE DES BALISES <p>
        print(len(toutP))
        #JE VÉRIFIE TOUS LES <p> DANS LE CODE HTML DES PAGES DE CONTRAT DÉTAILLÉ. JE REMARQUE QU'IL Y 16 BALISES <p>. JE VEUX TOUTES LES VALEURS SAUF CELLES EN DOUBLON, SOIT "Date", "Fournisseur" et "Description"
        
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
        #CE SONT TOUTES LES VALEURS DES PAGES DE CONTRAT DÉTAILLÉ, DONC LES INFOS DE TOUS LES HYPERLIENS, QUE J'AJOUTE À MON DICTIONNAIRE
        #PAR EXEMPLE LE NUMÉRO DE RÉFÉRENCE 'reference' CORRESPOND À LA CINQUIÈME BALISE <p> DU CODE SOURCE DES HYPERLIENS, ET AINSI DE SUITE
        
        print(contrat)
        
        table.append(contrat)
        #J'AJOUTE TOUTES LES INFOS À MON TABLEAU QUE J'AI CRÉÉ
        
    i = i+1
    #JE VEUX QUE LE COMPTEUR DANS LA LOUPE FASSE +1 PARCE QUE JE VEUX ENLEVER LA PREMIÈRE LIGNE DU TABLEAU DE LA PAGE WEB QUI NE SERT À RIEN


f1 = open(fichier, 'w')
#JE VEUX METTRE MES DONNÉES DANS UN FICHIER CSV. 'w' EST MARQUÉ POUR DIRE AU SYSTÈME D'ÉCRIRE (WRITE) UN FICHIER CSV

document = csv.DictWriter(f1,['date', 'fournisseur', 'description', 'reference', 'periode', 'methode invitation', 'marches pluriannuels', 'type document', 'modifications', 'valeur originale', 'valeur cumulative', 'valeur globale', 'commentaires'])
#JE VEUX ENREGISTRER LES DONNÉES DE MON DICTIONNAIRE ET POUVOIR L'OUVRIR EN CONSERVANT MON DICTIONNAIRE. C'EST POURQUOI J'UTILISE DictWriter AU LIEU DE writer

document.writeheader()
#.WRITEHEADER AIDE AU BON FONCTIONNAIRE DE DictWriter. ÇA PERMET D'ÉCRIRE DES RANGÉES QUI CONTIENNENT LES CATÉGORIES DE DONNÉES QUI SE TROUVENT DANS MON DICTIONNAIRE 


for contrat in table:
    #JE CRÉE UNE LOUPE POUR ENREGISTRER LE TABLEAU DE LA PAGE WEB EN CSV
    document.writerow(contrat)
    #.WRITEROW EST LA FONCTION POUR ÉCRIRE DES LIGNES DE DONNÉES DANS LE FICHIER CSV
    
    
    


#SCRIPT RÉALISÉ LE 29 OCTOBRE 2016 PAR SARAH DAOUST-BRAUN 

