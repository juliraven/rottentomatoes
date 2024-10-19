import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px

dane = pd.read_excel('dane1.csv', header=1)

sentiment_counts = dane['sentiment'].value_counts().reset_index()
sentiment_counts.columns = ['sentiment', 'count']

fig = px.pie(sentiment_counts, 
             values='count', 
             names='sentiment', 
             title='Podział recenzji wg sentymentu')

st.plotly_chart(fig)

