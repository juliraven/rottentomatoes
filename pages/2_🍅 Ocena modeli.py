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
    st.write("bedzie")

    # Tworzenie macierzy konfuzji
    cm = confusion_matrix(y_test, y_pred, labels=['Negative', 'Positive'])

    # Tworzenie wykresu macierzy konfuzji w Plotly
    fig = px.imshow(cm, 
                labels=dict(x="Predicted", y="Actual", color="Count"), 
                x=['Negative', 'Positive'], 
                y=['Negative', 'Positive'],
                text_auto=True,  # Wyświetla liczby w komórkach
                color_continuous_scale='Blues')  # Paleta kolorów

    fig.update_layout(title="Macierz konfuzji", title_x=0.5)  # Centrowanie tytułu
    st.plotly_chart(fig)

with tab2:
    st.write("bedzie vol2")

