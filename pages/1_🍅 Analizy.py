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

sentiment_counts = dane1['sentiment'].value_counts().reset_index()
sentiment_counts.columns = ['sentiment', 'count']

custom_colors = ['forestgreen', 'indianred', 'deepskyblue']  

fig = px.pie(sentiment_counts, 
             values='count', 
             names='sentiment', 
             title='Podział recenzji wg sentymentu',
             width=800,  
             height=500,
             color_discrete_sequence=custom_colors)

fig.update_traces(textfont_size=20)
st.plotly_chart(fig, use_container_width=True)


wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='plasma').generate(dane2)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.write('Chmura słów dla recenzji o negatywnym sentymencie')
st.pyplot(plt)



