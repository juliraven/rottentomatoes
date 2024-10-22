import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import confusion_matrix

st.markdown(
    """
    <style>
    .emoji-top {
        margin-top: -20px; /* Zmniejszenie marginesu górnego */
    }
    </style>
    
    <div style="text-align: left;">
        <h1>🍅 Ocena modeli</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown('######')

tab1, tab2 = st.tabs(["Naiwny klasyfikator Bayesa", "Regresja logistyczna"])

with tab1:
    
    dane8 = pd.read_csv('dane8.csv')

    cm = confusion_matrix(dane8['y_test'], dane8['y_pred'], labels=['Negative', 'Neutral', 'Positive'])

    fig = px.imshow(cm, labels=dict(x="Przewidywane", y="Rzeczywiste", color="Liczność"), 
                        x=['Negative', 'Neutral', 'Positive'], 
                        y=['Negative', 'Neutral', 'Positive'],
                        text_auto=True, 
                        color_continuous_scale='Blues')  
    
    fig.update_layout(title="Macierz pomyłek", title_x=0.5)
    st.plotly_chart(fig)

    
with tab2:
    st.write("bedzie vol2")

