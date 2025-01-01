import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Analiza sentymentu", layout="wide")

st.markdown(
    """
    <style>
    .emoji-top {
        margin-top: -20px; /* Zmniejszenie marginesu górnego */
    }
    </style>
    
    <div style="text-align: center;">
        <h1 class="emoji-top">🍅 🍅 🍅</h1> 
        <h2>Analiza sentymentu na podstawie recenzji użytkowników strony <br>Rotten Tomatoes</h2>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        width: 300px;  /* Ustaw stałą szerokość */
        min-width: 300px;  /* Minimalna szerokość */
        max-width: 300px;  /* Maksymalna szerokość */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.image('tomato.png', width=300)
st.markdown('######')
st.markdown('<span style="font-size: 24px">Strona ta poświęcona jest analizie sentymentu zbioru zawierającego recenzje filmów napisane przez krytyków na stronie Rotten Tomatoes. Znajdują się tutaj wizualizacje informacji zawartych w tym zbiorze, a także oceny modeli zbudowanych w oparciu o dane ze zbioru. Użytkownik ma również możliwość przetestowania działania modeli na dwa sposoby :</span>', unsafe_allow_html=True)
st.markdown('<span style="font-size: 24px">- może wprowadzić własną recenzję i zobaczyć przewidywany sentyment</span>', unsafe_allow_html=True)
st.markdown('<span style="font-size: 24px">- może podać link do recenzji konkretnego filmu/serialu ze strony Rotten Tomatoes i zobaczyć jaki sentymenty przewiduje dla nich model.</span>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    /* Zmiana kolorów obramowania i tła */
    .bordered-text {
        border: 2px solid #1c6429; /* Zielone obramowanie (primaryColor) */
        padding: 20px; /* Odstępy wewnętrzne */
        border-radius: 10px; /* Zaokrąglenie rogów */
        background-color: #580707; /* Czerwone tło (secondaryBackgroundColor) */
        color: #ecdede; /* Kolor tekstu (textColor) */
        margin: 20px 0; /* Margines wokół obramowanego tekstu */
        font-size: 20px; /* Rozmiar czcionki */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Tekst z obramowaniem
st.markdown('<div class="bordered-text">To jest tekst z obramowaniem. Możesz tu dodać dowolne informacje, które chcesz wyróżnić na stronie.</div>', unsafe_allow_html=True)
