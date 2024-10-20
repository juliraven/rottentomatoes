import streamlit as st
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px

dane1 = pd.read_csv('dane1.csv')
dane2 = pd.read_csv('dane2.csv')

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
st.markdown('### Podział recenzji wg sentymentu')
st.plotly_chart(fig, use_container_width=True)

st.markdown('### Liczba recenzji według gatunku i typu recenzji')
fig1 = px.bar(dane2, x='genres', y='count', color='review_type', barmode='group',
             labels={'count': 'Liczba recenzji', 'genres': 'Gatunki', 'review_type': 'Typ recenzji'})

st.plotly_chart(fig1)

st.markdown('### Chmury słów dla recenzji o danym sentymencie')
c1, c2, c3 = st.columns((2,2,2))

c1.image("negatywne.png", caption="Chmura słów dla recenzji o negatywnym sentymencie")
c2.image("pozytywne.png", caption="Chmura słów dla recenzji o pozytywnym sentymencie")
c3.image("neutralne.png", caption="Chmura słów dla recenzji o neutralnym sentymencie")




