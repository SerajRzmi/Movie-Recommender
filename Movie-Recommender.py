#Libraries
import numpy as np
import pandas as pd
import re
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import streamlit as st

## Data preprocessing
data = pd.read_table('/Users/seraj/Desktop/MoviesII.tsv')
data = data.drop(['1','2','Country','Language'],axis = 1)
data = data.dropna()
for i in range(len(data)):
    string = data.Genres.iloc[i]
    string = re.sub('\w+":','',string)
    string = re.sub('"/m/','',string)
    data.Genres.iloc[i] = string
    
    date = str(data.Release.iloc[i])
    date = re.findall('\d+$',date)
    date = date[0]
    data.Release.iloc[i] = date

data.Release = data.Release.astype(int)
data = data[data.Release>=2000]

aggrigate = []
for i in range(len(data)):
    revenue = str(data.Renevue.iloc[i])
    genres  = str(data.Genres.iloc[i])
    aggrigate.append(str(revenue+' '+ genres))
    
data['aggrigate'] = aggrigate
data['indx'] = list(range(len(data)))
data.set_index('indx',inplace = True)

## Cosine Similarity 
matrix = CountVectorizer().fit_transform(data.aggrigate)
cs = cosine_similarity(matrix)

movie_name = st.text_input(label = 'Movie Name',
    value = "Adam")

## recommender function
def recommender(movie_name):
    movie_index = data[data.Name == movie_name].index.values[0]
    scores = list(enumerate(cs[movie_index]))
    sorted_scores = sorted(scores, key=lambda x : x[1] ,reverse = True)
    movie_list = []
    for item in sorted_scores[1:7]:
        movie_list.append(data[data.index==item[0]]['Name'].values[0])
    return movie_list




st.write('movie name is: ',movie_name,"\u2713")
try:
    st.write(recommender(movie_name))
except IndexError :
    st.write('this Movie not in dataset')
