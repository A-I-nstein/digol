#####-----importing neccessary libraries-----#####

import os
import requests
import pinecone
import numpy as np
import pandas as pd
import tensorflow_hub as hub
from bs4 import BeautifulSoup

pinecone.init(
    api_key = os.environ.get("PINECONE_API_KEY"),
    environment = os.environ.get("PINECONE_ENVIRONMENT")
)
index = pinecone.Index(os.environ.get("index_name"))
model = hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim128/2")

#####-----Backend Functions-----#####

def to_float(n):
  return float(n)

def get_top_n(query, n):
    embedding = model(list(query))
    embedding = list(map(to_float, list((np.array(embedding[0])))))
    result = index.query([embedding], top_k=n, include_metadata=True)
    return result

def load_base_notes():
    notes_data = pd.read_csv('processed_data/base_notes.csv')
    base_notes = []
    for i in notes_data['base_notes']:
        base_notes.append(i)
    return base_notes

def load_fragrances():
    fragrances_data = pd.read_csv('processed_data/title.csv')
    fragrances = []
    for i in fragrances_data['title']:
        fragrances.append(i)
    return fragrances

def find_link(brand, title):
    url = 'https://www.google.com/search?q=' + brand+' '+title + '&tbm=isch&source=hp&biw=2&bih=2&ei=DKZaYfDjBorN1sQP1J6LsA4&ved=0ahUKEwjwmbmBl7DzAhWKppUCHVTPAuYQ4dUDCAc&uact=400&oq=images&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQMyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQMyCAgAEIAEELEDMgsIABCABBCxAxCDATIFCAAQgAQ6CAgAELEDEIMBUIEgWNImYOspaABwAHgAgAFViAHGA5IBATaYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABAA&sclient=img'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_links = soup.find_all('img')
    for tag in image_links:
        link = tag.get('src')
        if(link != None and  link[0:4] == 'http'):
            return(link)

def base_notes_to_fragrance(base_notes, gender, age):
    query = ''.join(base_notes) + ' ' + gender + ' ' + age
    suggested_fragrances = {}
    result = get_top_n(query, 3)
    count = 0
    for record in result['matches']:
        suggested_fragrances[count] = [
                                        record['metadata']['title'],
                                        record['metadata']['accords'],
                                        record['metadata']['secondary notes'],
                                        record['metadata']['gender'],
                                        record['metadata']['age'],
                                        find_link(record['metadata']['brand'], record['metadata']['title']),
                                        record['metadata']['brand']
                                        ]
        count = count+1
    return (suggested_fragrances)

def fragrance_to_fragrance(fragrance):
    perfumes = pd.read_csv('processed_data/molecule_perfume_final_with_sec_notes.csv')
    data = perfumes.loc[perfumes['title']==fragrance]
    query = data["age"] + " " + data["gender"] + " " + data["accords"] + " " + data["secondary notes"]
    result = get_top_n(query, 3)
    suggested_fragrances = {}
    count = 0
    for record in result['matches']:
        suggested_fragrances[count] = [
                                        record['metadata']['title'],
                                        record['metadata']['accords'],
                                        record['metadata']['secondary notes'],
                                        record['metadata']['gender'],
                                        record['metadata']['age'],
                                        find_link(record['metadata']['brand'], record['metadata']['title']),
                                        record['metadata']['brand']
                                        ]
        count = count+1
    return (suggested_fragrances)
