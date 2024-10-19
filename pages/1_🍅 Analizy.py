import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px

dane = pd.read_csv('dane1.csv')

sentiment_counts = dane['sentiment'].value_counts().reset_index()
sentiment_counts.columns = ['sentiment', 'count']

fig = px.pie(sentiment_counts, 
             values='count', 
             names='sentiment', 
             title='Podział recenzji wg sentymentu')

st.plotly_chart(fig, use_container_width=True)

