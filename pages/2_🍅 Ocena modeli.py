import streamlit as st
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px


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

from streamlit_option_menu import option_menu

# Menu przypominające zakładki
selected = option_menu(
    menu_title=None,  # Tytuł menu, jeśli nie jest potrzebny, ustaw na None
    options=["Tab 1", "Tab 2", "Tab 3"],  # Zakładki
    icons=["house", "gear", "envelope"],  # Ikony dla zakładek (opcjonalne)
    menu_icon="cast",  # Ikona menu (opcjonalne)
    default_index=0,  # Domyślnie zaznaczona zakładka
    orientation="horizontal",  # Układ poziomy (horizontal) lub pionowy (vertical)
)

# Warunkowe wyświetlanie treści w zależności od aktywnej zakładki
if selected == "Tab 1":
    st.write("This is Tab 1")
    st.sidebar.empty()  # Brak sidebaru dla Tab 1
elif selected == "Tab 2":
    st.write("This is Tab 2")
    with st.sidebar:
        st.write("This is the sidebar for Tab 2")  # Sidebar tylko dla Tab 2
elif selected == "Tab 3":
    st.write("This is Tab 3")
    st.sidebar.empty()  # Brak sidebaru dla Tab 3


