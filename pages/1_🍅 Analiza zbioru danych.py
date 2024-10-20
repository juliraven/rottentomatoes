import streamlit as st
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px

dane1 = pd.read_csv('dane1.csv')
dane2 = pd.read_csv('dane2.csv')
dane3 = pd.read_csv('dane3.csv')
dane4 = pd.read_csv('dane4.csv')

st.markdown(
    """
    <style>
    .emoji-top {
        margin-top: -20px; /* Zmniejszenie marginesu górnego */
    }
    </style>
    
    <div style="text-align: left;">
        <h1>🍅 Analiza zbioru danych</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown('###')

st.markdown('### Chmury słów dla recenzji o danym sentymencie')
c1, c2, c3 = st.columns((2,2,2))
c1.image("negatywne.png", caption="Chmura słów dla recenzji o negatywnym sentymencie")
c2.image("pozytywne.png", caption="Chmura słów dla recenzji o pozytywnym sentymencie")
c3.image("neutralne.png", caption="Chmura słów dla recenzji o neutralnym sentymencie")

st.markdown('###')

a1, a2 = st.columns((2,2))
sentiment_counts = dane1['sentiment'].value_counts().reset_index()
sentiment_counts.columns = ['sentiment', 'count']

custom_colors = ['forestgreen', 'indianred', 'deepskyblue']  

fig = px.pie(sentiment_counts, 
             values='count', 
             names='sentiment', 
             width=800,  
             height=500,
             color_discrete_sequence=custom_colors)

fig.update_traces(textfont_size=20)
a1.markdown('### Podział recenzji wg sentymentu')
a1.plotly_chart(fig, use_container_width=True)

custom_colors1 = ['red', 'rgb(61,94,47)']  

fig1 = px.pie(dane4, 
             values='review_type', 
             names='index', 
             width=800,  
             height=500,
             color_discrete_sequence=custom_colors1)

fig1.update_traces(textfont_size=20)
a2.markdown('### Podział recenzji wg typu')
a2.plotly_chart(fig1, use_container_width=True)
st.markdown('###')

gatunki = dane2['genres'].unique()
wybierz_gatunek = st.selectbox('Wybierz gatunek :', gatunki)
filtered_df = dane2[dane2['genres'] == wybierz_gatunek]
filtered_df1 = dane3[dane3['genres'] == wybierz_gatunek]
b1, b2 = st.columns((2,2))

fig2 = px.pie(filtered_df1, values='count', names='sentiment', color='sentiment',
             width=800,  
             height=500,
             color_discrete_sequence=custom_colors)

fig2.update_traces(textfont_size=20)
b1.markdown('### Podział recenzji wg sentymentu dla wybranego gatunku')
b1.plotly_chart(fig2, use_container_width=True)

fig3 = px.pie(filtered_df, values='count', names='review_type', color='review_type',
             width=800,  
             height=500,
             color_discrete_sequence=custom_colors1)

fig3.update_traces(textfont_size=20)
b2.markdown('### Podział recenzji wg typu dla wybranego gatunku')
b2.plotly_chart(fig3, use_container_width=True)






