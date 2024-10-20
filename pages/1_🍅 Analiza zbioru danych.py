import streamlit as st
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px

dane1 = pd.read_csv('dane1.csv')

st.markdown(
    """
    <style>
    .emoji-top {
        margin-top: -20px; /* Zmniejszenie marginesu górnego */
    }
    </style>
    
    <div style="text-align: left;">
        <h2>Analiza zbioru danych</h2>
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
st.title('Podział recenzji wg sentymentu')
st.plotly_chart(fig, use_container_width=True)

c1, c2, c3 = st.columns((2,2,2))

st.title('Chmury słów dla recenzji o danym sentymencie')
c1.image("negatywne.png", caption="Chmura słów dla recenzji o negatywnym sentymencie")
c2.image("pozytywne.png", caption="Chmura słów dla recenzji o pozytywnym sentymencie")
c3.image("neutralne.png", caption="Chmura słów dla recenzji o neutralnym sentymencie")


