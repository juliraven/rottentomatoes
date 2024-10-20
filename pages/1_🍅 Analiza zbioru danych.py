import streamlit as st
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px

dane1 = pd.read_csv('dane1.csv')

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

st.title('Chmury słów dla recenzji o danym sentymencie')
st.image("negatywne.png", caption="Chmura słów dla recenzji o negatywnym sentymencie")
st.image("pozytywne.png", caption="Chmura słów dla recenzji o pozytywnym sentymencie")
st.image("neutralne.png", caption="Chmura słów dla recenzji o negutralnym sentymencie")


