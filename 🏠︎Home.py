import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(page_title="Analiza Sentymentu")

st.markdown(
    """
    <style>
    .emoji-top {
        margin-top: -20px; /* Zmniejszenie marginesu górnego */
    }
    </style>
    
    <div style="text-align: center;">
        <h1 class="emoji-top">🍅 🍅 🍅</h1> 
        <h2>Analiza sentymentu recenzji filmowych na podstawie recenzji użytkowników strony</h2>
    </div>
    """, 
    unsafe_allow_html=True
)

st.image('tomato.png', use_column_width=True)

