import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

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

tab1, tab2 = st.tabs(["Naiwny klasyfikator Bayesa", "Sieć neuronowa"])

with tab1:

    st.markdown('######')
    
    st.markdown('### Macierz pomyłek')
    
    dane = pd.read_csv('dane_model1.csv')

    trafnosc = accuracy_score(dane['y_test'], dane['y_pred'])

    cm = confusion_matrix(dane['y_test'], dane['y_pred'], labels=['Negatywne', 'Pozytywne'])

    fig = px.imshow(cm, labels=dict(x="Przewidywane", y="Rzeczywiste", color="Liczność"), 
                        x=['Negatywne', 'Pozytywne'], 
                        y=['Negatywne', 'Pozytywne'],
                        text_auto=True, 
                        color_continuous_scale='Reds')  
    
    fig.update_layout(width=800, height=600,
    xaxis_title="Przewidywane",
    xaxis=dict(title='Przewidywane', title_standoff=50),
    yaxis=dict(title="Rzeczywiste", title_standoff=50),
    font=dict(size=16) )

    st.plotly_chart(fig)

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    sensitivity = tp/(fn+tp)
    specificity = tn/(tn+fp)
    precision = tp/(fp+tp)
    print('Czułość :', str('{:04.2f}'.format(sensitivity*100))+'%')
    print('Specyficzność :', str('{:04.2f}'.format(specificity*100))+'%')
    print('Prezycja :', str('{:04.2f}'.format(precision*100))+'%')

    st.subheader('Trafność')
    c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = st.columns((2,2,2,2,2,2,2,2,2,2))
    c1.success(f'**{round(trafnosc * 100, 1)}%**')


    st.markdown('######')

    


with tab2:

    st.markdown('######')
    
    st.markdown('### Macierz pomyłek')
    
   
