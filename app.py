# -*- coding: utf-8 -*-
# @Author: prateek
# @Date:   2021-03-06 21:48:25
# @Last Modified by:   prateek
# @Last Modified time: 2021-03-15 18:14:55

import streamlit as st 
import numpy as np 
import time
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

st.markdown("<h1 style='text-align: center;'>RECOMMENDIFY</h1>", unsafe_allow_html=True)
st.markdown("**Recommendify** is a one-stop solution to movie recommendation. It uses content based recommendation to handle the cold start problem along with a weighted average to maintain the balance between the movies. The movies are recommended based on their content and genres. Hope you like it.!!!")

def give_top_weight_avg(data):
	x = data.sort_values(by=['weighted_average'],ascending=False)
	x = x.reset_index(drop=True)
	return x
def give_top_pop(data):
	x = data.sort_values(by=['popularity'],ascending=False)
	x = x.reset_index(drop=True)
	return x
def give_rec(title,sig=None) :
	idx = indices[title]
	sig_scores = list(enumerate(sig[idx]))
	sig_scores = sorted(sig_scores,key=lambda x: x[1],reverse=True)
	movie_ids = [i[0] for i in sig_scores]
	return data.iloc[movie_ids]

def display(val,x):
	# st.dataframe(val)
	st.markdown('# '+str(x)+' - Movie: ' + str(val['original_title']))
	# st.write(type(val['tagline']))
	if not pd.isna(val['tagline']):
		tag = '## '+str(val['tagline'])
		st.markdown(tag)
	st.markdown('		**Genres:** ' + str(val['genres'][1:len(val['genres'])-1]))
	st.markdown('		**Runtime:** '+ str(int(val['runtime']//60)) +'hr '+str(int(val['runtime']%60))+'min')
	st.markdown('		**Weighted Average:** '+ str(np.round(val['weighted_average'])))
	st.markdown('		**Popularity:** '+ str(np.round(val['popularity'])))
	st.markdown(val['overview'])


data = pd.read_csv('data.csv')
tfv = TfidfVectorizer(min_df=3,max_features=None,strip_accents='unicode',analyzer='word',token_pattern='\w{1,}',
                      ngram_range=(1,3),stop_words='english')
tfv_matrix = tfv.fit_transform(data['overview'])
sig = sigmoid_kernel(tfv_matrix,tfv_matrix)
indices = pd.Series(data.index,index=data['original_title']).drop_duplicates()	

top_movies_avg = give_top_weight_avg(data)
top_movies_pop = give_top_pop(data)

st.sidebar.markdown("""## Recommendify""")
st.sidebar.markdown("""Recommendify uses the overview of movies along with pearson similarity to extract similar movies to the chosen movies.""")


# st.sidebar.markdown("""Please select the number of movies :""")
count = st.sidebar.slider("Number of movies to predict :", 1, 20, 10, 1)
st.markdown("""###### Note : Just start typing in the box and it will filter automatically. {You dont need to press backspace}""")
movies_list = ['-']
for movie in data['original_title'].unique():
	movies_list.append(movie)

st.write("")
select_movie = st.selectbox('Select a movie',movies_list)
col1, col2, col3 , col4, col5 = st.beta_columns(5)
with col1:
	pass
with col2:
	pass
with col4:
	pass
with col5:
	pass
with col3 :
	recommend = st.button('Recommend')

if recommend and select_movie !='-':
	my_bar = st.progress(0)
	for percent_complete in range(100):
		time.sleep(0.01)
		my_bar.progress(percent_complete + 1)
	st.balloons()

	recommendations = give_rec(select_movie,sig).reset_index(drop=True)
	for i in range(1,count+1):
		display(recommendations.iloc[i],i)
	total = 0
	pred = 0
	with open('counts.txt','r+') as f:
		data = f.readlines()
		total = int(data[0].split(',')[0])
		pred = int(data[0].split(',')[1])
	f.close()
	total+=1
	pred+=count
	line_to_write = str(total)+','+str(pred)
	with open('counts.txt','w+') as f:
		f.write(line_to_write)
	f.close()

elif recommend and select_movie=='-':
	st.error('Please select a valid movie')
	st.markdown("""## Top Rated Movies using a Weighted Average """)
	x = top_movies_avg.head(count)[['original_title','weighted_average','popularity']]
	x.columns = ['Title','Weighted Average','Popularity']
	st.dataframe(x)
	x = top_movies_pop.head(count)[['original_title','popularity','weighted_average']]
	x.columns = ['Title','Popularity','Weighted Average']
	st.markdown("""## Top Rated Movies based on Popularity """)
	st.dataframe(x)

else:
	st.markdown("""## Top Rated Movies using a Weighted Average """)
	x = top_movies_avg.head(count)[['original_title','weighted_average','popularity']]
	x.columns = ['Title','Weighted Average','Popularity']
	st.dataframe(x)
	x = top_movies_pop.head(count)[['original_title','popularity','weighted_average']]
	x.columns = ['Title','Popularity','Weighted Average']
	st.markdown("""## Top Rated Movies based on Popularity """)
	st.dataframe(x)

with open('counts.txt','r+') as f:
            data = f.readlines()
            # print(data)
            st.sidebar.write("""<font color=‘blue’>Total App Runs :</font> **""" +data[0].split(',')[0]+"**", unsafe_allow_html=True)
            st.sidebar.markdown("""<font color=#0e6b0e>Total Movies Recommended:</font> **"""+data[0].split(',')[1]+"**", unsafe_allow_html=True)
f.close()


st.sidebar.markdown("""#### Recommendify is built and maintained by **Prateek Agrawal**. Please contact in case of queries or just to say Hi!!!.""")
github = '[GitHub](http://github.com/prateekagrawaliiit)'
linkedin = '[LinkedIn](https://www.linkedin.com/in/prateekagrawal1405/)'
email = '<a href="mailto:prateekagrawaliiit@gmail.com">Email</a>'
st.sidebar.markdown("""""")
st.sidebar.markdown(github, unsafe_allow_html=True)
st.sidebar.markdown(linkedin, unsafe_allow_html=True)
st.sidebar.markdown(email, unsafe_allow_html=True)