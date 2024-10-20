import streamlit as st

st.set_page_config(page_title="Analiza Sentymentu", layout="wide")

st.markdown(
    """
    <style>
    .emoji-top {
        margin-top: -20px; /* Zmniejszenie marginesu górnego */
    }
    </style>
    
    <div style="text-align: center;">
        <h1 class="emoji-top">🍅 🍅 🍅</h1> 
        <h2>Analiza sentymentu recenzji filmowych na podstawie recenzji użytkowników strony Rotten Tomatoes</h2>
    </div>
    """, 
    unsafe_allow_html=True
)

st.sidebar.image('tomato.png', width=300)

st.markdown('<span style="font-size: 24px">Strona ta poświęcona jest </span>', unsafe_allow_html=True)
