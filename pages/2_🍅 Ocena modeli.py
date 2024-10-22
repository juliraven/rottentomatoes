import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import confusion_matrix, accuracy_score

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

    st.markdown('######')
    
    st.markdown('### Macierz pomyłek')
    
    dane8 = pd.read_csv('dane8.csv')

    trafnosc = accuracy_score(dane8['y_test'], dane8['y_pred'])

    cm = confusion_matrix(dane8['y_test'], dane8['y_pred'], labels=['Negative', 'Neutral', 'Positive'])

    fig = px.imshow(cm, labels=dict(x="Przewidywane", y="Rzeczywiste", color="Liczność"), 
                        x=['Negative', 'Neutral', 'Positive'], 
                        y=['Negative', 'Neutral', 'Positive'],
                        text_auto=True, 
                        color_continuous_scale='Reds')  
    
    fig.update_layout(width=800, height=600,
    xaxis_title="Przewidywane",
    xaxis=dict(title='Przewidywane', title_standoff=50),
    yaxis=dict(title="Rzeczywiste", title_standoff=50),
    font=dict(size=16) )

    st.plotly_chart(fig)

    st.subheader('Trafność :')
    st.success(f'**Trafność: {round(trafnosc * 100, 3)}%**')

with tab2:

    st.markdown('######')
    
    st.markdown('### Macierz pomyłek')
    
    dane9 = pd.read_csv('dane9.csv')

    trafnosc = accuracy_score(dane9['y_test'], dane9['y_pred'])

    cm = confusion_matrix(dane9['y_test'], dane9['y_pred'], labels=['Negative', 'Neutral', 'Positive'])

    fig1 = px.imshow(cm, labels=dict(x="Przewidywane", y="Rzeczywiste", color="Liczność"), 
                        x=['Negative', 'Neutral', 'Positive'], 
                        y=['Negative', 'Neutral', 'Positive'],
                        text_auto=True, 
                        color_continuous_scale='Reds')  
    
    fig1.update_layout(width=800, height=600,
    xaxis_title="Przewidywane",
    xaxis=dict(title='Przewidywane', title_standoff=50),
    yaxis=dict(title="Rzeczywiste", title_standoff=50),
    font=dict(size=16) )

    st.plotly_chart(fig1)

