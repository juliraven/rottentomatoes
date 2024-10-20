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
