#importation des librairies et biblotheques
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from time import time
from IPython.display import clear_output
from warnings import warn
from ast import Break
 
import pandas as pd 

# Modification liée au changement de structure de l'url de recherche
# L'url n'est plus classée par page mais par premier élément
# Je constate que chaque page de recherche contient toujours 50 films
# Donc voici le nouvel url de recherche avec les premier film de chaque page qui prendra les valeurs 1, 51, 101,..:
# 'http://www.imdb.com/search/title?release_date='+ {ANNEE}+'&sort=num_votes,desc&start='+{NUMERO}

numero_page = [str(i) for i in range(1,300,50)]
 
urls_annee = [str(i) for i in range(2010,2023)]

#Je declare les listes
noms = []
annees = []
notes_critiques =[]
metascores = []
votes = []

#Je prépare l'affichage des boucles
start_time = time()
requests = 0

#Pour chaque année de l'intervalle 2018-2023
for annee in urls_annee:
  #boucle sur  les contenant des premiers films des pages de 1 à 6
  for page in numero_page:
    #Faire une requête GET
    response = get('http://www.imdb.com/search/title?release_date='+annee+'&sort=num_votes,desc&start='+page)
	        
    sleep(randint(3,5)) #Pause la boucle de 2 à 5 secondes
	        
    #Affichges des informations sur les requêtes
    requests += 1
    elapsed_time = time() - start_time
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
	        
    #Avertissement si le code status est différent de 200
    if response.status_code != 200:
      warn('Request: {}; Status code: {}'.format(requests, response.status_code))
	            
    # Stoppage de la boucle si le nombre de requêtes est supérieur à 50
    if requests > 80:
      warn('Nombre de requêtes trop important')
      break
	            
    #Extraction de l' HTML avec BeautifulSoup
    html_soup = BeautifulSoup(response.text, 'html.parser')
        
    #Sélectionner les 50 films de chaque page (contenus_film)
    contenus_film = html_soup.find_all('div', class_="lister-item mode-advanced")
	        
    #Boucle pour chaque pages(contenus_film)
    for contenue in contenus_film:
      #Si le film a un Metascore
      if contenue.find('div', class_='ratings-metascore') is not None:
        
        #scraping du titre
        nom = contenue.h3.a.text
        noms.append(nom)
	                
        #scraping de l'année des films
        annee = contenue.h3.find('span', class_='lister-item-year').text
        annees.append(annee)
	                
        #scraping de la note critiques
        note_critique = float(contenue.strong.text) #convertion en float
        notes_critiques.append(note_critique)
	                
        #scraping du Metascore
        metascore = contenue.find('span', class_='metascore').text
        metascores.append(int(metascore))

        #scraping le nombre de votes
        vote = contenue.find('span', attrs = {'name':'nv'})['data-value']
        votes.append(int(vote))


#creaction de dataframme
donnees_films = pd.DataFrame({
  'Titre de films': noms,
  'Années': annees,
  'Moy de la note': notes_critiques,
  'Metas  scores': metascores,
  'Le Nombre de votes': votes
  })

#Convertison en fichier CSV
donnees_films.to_csv('Mes_donnes_scrape_imdb.csv')