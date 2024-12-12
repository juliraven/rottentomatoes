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

    cm = confusion_matrix(dane['y_test'], dane['y_pred'], labels=[0,1])

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

    tn, fp, fn, tp = confusion_matrix(dane['y_test'], dane['y_pred']).ravel()
    sensitivity = tp/(fn+tp)
    specificity = tn/(tn+fp)
    precision = tp/(fp+tp)

    text_color = "#FF5733"  
    font_size = "24px"      

    trafnosc_rounded = round(trafnosc * 100)
    sensitivity_rounded = round(sensitivity * 100)
    specificity_rounded = round(specificity * 100)
    precision_rounded = round(precision * 100)

    st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Trafność : {trafnosc_rounded*100:04.2f}%</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Czułość : {sensitivity_rounded*100:04.2f}%</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Specyficzność : {specificity_rounded*100:04.2f}%</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Precyzja : {precision_rounded*100:04.2f}%</p>", unsafe_allow_html=True)


    st.markdown('######')

with tab2:

    st.markdown('######')
    
    st.markdown('### Macierz pomyłek')
    
   
