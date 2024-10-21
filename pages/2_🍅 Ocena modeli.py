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

page = st.selectbox("Choose a page", ["Page 1", "Page 2", "Page 3"])

# Warunkowe wyświetlanie treści
if page == "Page 1":
    st.write("This is Page 1")
    st.sidebar.empty()  # Ukrycie sidebaru na stronie 1
elif page == "Page 2":
    st.write("This is Page 2")
    with st.sidebar:
        st.write("This is the sidebar for Page 2")  # Sidebar widoczny tylko na stronie 2
elif page == "Page 3":
    st.write("This is Page 3")
    st.sidebar.empty()  # Ukrycie sidebaru na stronie 3
