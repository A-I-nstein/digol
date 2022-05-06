#####-----importing neccessary libraries-----#####

import spacy
import requests
import numpy as np
import pandas as pd
from math import sqrt
from bs4 import BeautifulSoup

nlp = spacy.load('models/en_core_web_md/en_core_web_md-3.2.0')

#####-----Backend Functions-----#####

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

def find_max_3(score):
    score = list(score)
    max_score_ind = []
    for i in range(3):
        max_score_ind.append(score.index(max(score)))
        score[max_score_ind[i]] = 0
    return(max_score_ind)

def find_top_200(score):
    score = list(score)
    max_score_ind = []
    score[score.index(max(score))] = 0
    for i in range(200):
        max_score_ind.append(score.index(max(score)))
        score[max_score_ind[i]] = 0
    return(max_score_ind)

def squared_sum(x):
    return round(sqrt(sum([a*a for a in x])),3)

def cos_similarity(x,y):
    numerator = sum(a*b for a,b in zip(x,y))
    denominator = squared_sum(x)*squared_sum(y)
    return round(numerator/float(denominator),3)

def find_link(brand, title):
    url = 'https://www.google.com/search?q=' + brand+' '+title + '&tbm=isch&source=hp&biw=2&bih=2&ei=DKZaYfDjBorN1sQP1J6LsA4&ved=0ahUKEwjwmbmBl7DzAhWKppUCHVTPAuYQ4dUDCAc&uact=400&oq=images&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQMyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQMyCAgAEIAEELEDMgsIABCABBCxAxCDATIFCAAQgAQ6CAgAELEDEIMBUIEgWNImYOspaABwAHgAgAFViAHGA5IBATaYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABAA&sclient=img'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_links = soup.find_all('img')
    image_data = []
    for tag in image_links:
        link = tag.get('src')
        if(link != None and  link[0:4] == 'http'):
            return(link)

def base_notes_to_fragrance(base_notes, gender, age):
    data = ''.join(base_notes) + ' ' + gender + ' ' + age
    perfume = pd.read_csv('processed_data/molecule_perfume_final_with_sec_notes.csv')
    embeddings = np.load('processed_data/base notes/embeddings.npz')
    embeddings = embeddings['embeddings']
    embedding = nlp(data).vector
    scores = []
    for i in range(0, len(embeddings)):
        scores.append(cos_similarity(embedding, embeddings[i]))
    fragrance_indices = find_max_3(scores.copy())
    suggested_fragrances = {}
    count = 0
    for i in fragrance_indices:
        suggested_fragrances[count] = [
                                        perfume['title'][i],
                                        perfume['accords'][i],
                                        perfume['secondary notes'][i],
                                        perfume['gender'][i],
                                        perfume['age'][i],
                                        find_link(perfume['brand'][i], perfume['title'][i]),
                                        perfume['brand'][i]
                                        ]
        count = count+1
    return (suggested_fragrances)

def fragrance_to_fragrance(fragrance):
    perfume = pd.read_csv('processed_data/molecule_perfume_final_with_sec_notes.csv')
    mapping = pd.Series(perfume.index, index = perfume['title'])
    scores = np.load('processed_data/fragrance/scores_similarity_1.npz')
    scores = scores['scores']
    fragrance_index = mapping[fragrance]
    similarity_score = scores[fragrance_index]
    top_200_ind = find_top_200(similarity_score.copy())
    perfume_similarity_2 = perfume.iloc[top_200_ind].copy()
    perfume_similarity_2 = perfume_similarity_2.reset_index()
    data = []
    for ind, row in perfume_similarity_2.iterrows():
        data.append(str(row['secondary notes'].replace(',', ' ')))
    perfume_similarity_2['data'] = data
    sentences = list(perfume_similarity_2['data'])
    embeddings = [nlp(sentence).vector for sentence in sentences]
    secondary_note = perfume.at[fragrance_index, 'secondary notes']
    embedding = nlp(secondary_note).vector
    scores = []
    for i in range(0, len(embeddings)):
        scores.append(cos_similarity(embedding, embeddings[i]))
    fragrance_indices = find_max_3(scores.copy())
    print(fragrance_indices)
    suggested_fragrances = {}
    count = 0
    for i in fragrance_indices:
        suggested_fragrances[count] = [
                                        perfume_similarity_2['title'][i],
                                        perfume_similarity_2['accords'][i],
                                        perfume_similarity_2['secondary notes'][i],
                                        perfume_similarity_2['gender'][i],
                                        perfume_similarity_2['age'][i],
                                        find_link(perfume_similarity_2['brand'][i], perfume_similarity_2['title'][i]),
                                        perfume_similarity_2['brand'][i]
                                        ]
        count = count+1
    return (suggested_fragrances)
