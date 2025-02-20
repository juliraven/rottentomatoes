import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from streamlit_extras.app_logo import add_logo

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 57% 50%,rgba(94, 7, 7, 1), rgba(0, 0, 0, 1), rgba(128,33,33,1));
    background-blend-mode: multiply;
    background-size: cover;
    overflow: hidden; /* Prevent scrolling */
}

header[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

add_logo('logo.png', height=350)

st.sidebar.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            padding-top: 0px;
            padding: 10px;
            font-family: sans-serif;
            font-size: 18px;
        }

        [data-testid="stSidebarHeader"] {
            height: 20px;
            padding: 5px 10px; 
            margin: 0; 
            display: flex; 
            align-items: center;
            justify-content: center; 
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        width: 350px;  /* Ustaw stałą szerokość */
        min-width: 350px;  /* Minimalna szerokość */
        max-width: 350px;  /* Maksymalna szerokość */
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

selected = option_menu(
    menu_title=None,  
    options=["Naiwny klasyfikator Bayesa", "Sieć neuronowa"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal", 
)

if selected=="Naiwny klasyfikator Bayesa":

    st.markdown('###')

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

    col1, col2 = st.columns([1.5, 1])  
    
    with col1:
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
                      margin=dict(t=70, b=0),
                      coloraxis_showscale=False,
                      title="Macierz pomyłek", title_x=0.6, title_xanchor="center", title_font=dict(size=30, family="Arial, sans-serif", color="white"),
                      plot_bgcolor='rgba(0, 0, 0, 0)',  
                      paper_bgcolor='rgba(0, 0, 0, 0)')

        st.plotly_chart(fig)


    with col2:
        st.markdown('#')
        st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Trafność : {trafnosc_rounded}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Czułość : {sensitivity_rounded}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Specyficzność : {specificity_rounded}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Precyzja : {precision_rounded}%</p>", unsafe_allow_html=True)

if selected=="Sieć neuronowa":
    st.markdown('###')

    dane = pd.read_csv('dane_model3.csv')

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

    col1, col2 = st.columns([1.5, 1])  
    
    with col1:
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
                      margin=dict(t=70, b=0),
                      coloraxis_showscale=False,
                      title="Macierz pomyłek", title_x=0.6, title_xanchor="center", title_font=dict(size=30, family="Arial, sans-serif", color="white"),
                      plot_bgcolor='rgba(0, 0, 0, 0)',  
                      paper_bgcolor='rgba(0, 0, 0, 0)')

        st.plotly_chart(fig)


    with col2:
        st.markdown('#')
        st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Trafność : {trafnosc_rounded}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Czułość : {sensitivity_rounded}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Specyficzność : {specificity_rounded}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text_color}; font-size:{font_size};'>Precyzja : {precision_rounded}%</p>", unsafe_allow_html=True)
    
   
