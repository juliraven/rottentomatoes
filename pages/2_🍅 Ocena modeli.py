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

    dane = pd.read_csv('dane_model1.csv')

    trafnosc = accuracy_score(dane['y_test'], dane['y_pred'])
    cm = confusion_matrix(dane['y_test'], dane['y_pred'], labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    sensitivity = tp / (fn + tp)
    specificity = tn / (tn + fp)
    precision = tp / (fp + tp)

    text_color = "#FF5733"  
    font_size = "24px"     
    trafnosc_rounded = round(trafnosc * 100)
    sensitivity_rounded = round(sensitivity * 100)
    specificity_rounded = round(specificity * 100)
    precision_rounded = round(precision * 100)

    col1, col2 = st.columns([1, 1])  
    
    with col1:
        st.markdown("<h3 style='text-align: center; margin-top: -10px;'>Macierz pomyłek</h3>", unsafe_allow_html=True)
        fig = px.imshow(cm, labels=dict(x="Przewidywane", y="Rzeczywiste", color="Liczność"), 
                    x=['Negatywne', 'Pozytywne'], 
                    y=['Negatywne', 'Pozytywne'],
                    text_auto=True, 
                    color_continuous_scale='Reds')  
    
        fig.update_layout(width=600, height=600,
                      xaxis_title="Przewidywane",
                      xaxis=dict(title='Przewidywane', title_standoff=50),
                      yaxis=dict(title="Rzeczywiste", title_standoff=50),
                      font=dict(size=16),
                      margin=dict(t=0, b=0),
                      coloraxis_showscale=False)

        st.plotly_chart(fig)


    with col2:
        st.markdown('#')
        st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Trafność : {trafnosc_rounded}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Czułość : {sensitivity_rounded}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Specyficzność : {specificity_rounded}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Precyzja : {precision_rounded}%</p>", unsafe_allow_html=True)

with tab2:

    st.markdown('######')
    
    st.markdown('### Macierz pomyłek')
    
   
