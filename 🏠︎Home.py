import streamlit as st

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
        <h2>Analiza sentymentu recenzji filmowych na podstawie recenzji użytkowników strony Rotten Tomatoes</h2>
    </div>
    """, 
    unsafe_allow_html=True
)
