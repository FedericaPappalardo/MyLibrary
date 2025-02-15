import pandas as pd
import json
import csv
from pymongo import MongoClient

dbName = "myLibrary"
clientUrl = "mongodb://localhost:27017/"
client = MongoClient(clientUrl)
db = client[dbName]

def popolaDB(csvPath, collectionName):
    print("Popopolando " + collectionName)
    coll = db[collectionName]
    data = pd.read_csv(csvPath)
    payload = json.loads(data.to_json(orient='records'))
    coll.drop()
    coll.insert_many(payload)

def inizializzaDB():
    # GESTIONE CSV per le collection BOOKS, USER, RATING
    rootPath = "./dataset/"
    dataAE = pd.read_csv(rootPath + "processed_data.csv")

    # CREAZIONE CSV BOOKS
    print("*** INIZIO Creazione csv BOOKS_INFO ***")
    dfbook = dataAE[['isbn', 'book_title', 'book_author', 'year_of_publication','publisher','Category']].copy()  # Crea dataframe contenente solo le info sui libri
    dfbook = dfbook.drop_duplicates(['isbn'])
    dfbook.to_csv(rootPath + "books_info.csv", index=False)  # Converti dataframe in csv
    print("*** FINE Creazione csv BOOKS_INFO ***")

    # CREAZIONE CSV USER
    print("*** INIZIO Creazione csv USERS_INFO ***")
    dfuser = dataAE[['user_id', 'age', 'city', 'country','state']].copy()  # Crea dataframe contenente solo le info sugli utenti
    dfuser = dfuser.drop_duplicates(['user_id'])
    dfuser.to_csv(rootPath + "users_info.csv", index=False)  # Converti dataframe in csv
    print("*** FINE Creazione csv USERS_INFO ***")

    # CREAZIONE CSV RATING
    print("*** INIZIO Creazione csv RATINGS_INFO ***")
    dfrating = dataAE[['user_id', 'isbn', 'rating']].copy()  # Crea dataframe contenente solo le info sui ratings
    dfrating.to_csv(rootPath + "ratings_info.csv", index=False)  # Converti dataframe in csv
    print("*** FINE Creazione csv RATINGS_INFO ***")
    
   # CARICAMENTO SU MONGODB
    print("**** Popolamento table Book ***")
    popolaDB(rootPath + "books_info.csv", "book")
    print("**** Fine Popolamento table Book ***")
    print("**** Popolamento table USER ***")
    popolaDB(rootPath + "users_info.csv", "user")
    print("**** FINE Popolamento table User ***")
    print("**** Popolamento table Rating ***")
    popolaDB(rootPath + "ratings_info.csv", "rating")
    print("**** FINE Popolamento table Rating ***")

def checkInizializza():
    if dbName not in client.list_database_names():  # Se non trova il db, lo crea e carica il dataset
        inizializzaDB()
