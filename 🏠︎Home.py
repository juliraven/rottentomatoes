import streamlit as st

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

# Zaktualizowany CSS do stylizacji
st.markdown(
    """
    <style>
    /* Zmiana kolorów obramowania i tła z ładnymi rogami */
    .bordered-text {
        border: 3px solid #1c6429; /* Zielone obramowanie (primaryColor) */
        padding: 20px; /* Odstępy wewnętrzne (zmniejszone, aby tekst był bliżej tytułu) */
        border-radius: 15px; /* Zaokrąglenie rogów */
        background-color: #580707; /* Czerwone tło (secondaryBackgroundColor) */
        color: #ecdede; /* Kolor tekstu (textColor) */
        margin: 20px 0; /* Margines wokół obramowanego tekstu */
        font-size: 24px; /* Rozmiar czcionki */
        box-shadow: inset 0px 0px 5px rgba(0, 0, 0, 0.1); /* Wewnętrzny cień obramowania */
    }
    
    /* Styl dla listy z myślnikami */
    .list-item {
        font-size: 24px;
        margin-left: 20px; /* Wcięcie w liście */
        color: #ecdede;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Całość (tekst główny i lista z myślnikami) umieszczona w jednej ramce
st.markdown('''
    <div class="bordered-text">
        Strona ta poświęcona jest analizie sentymentu zbioru zawierającego recenzje filmów napisane przez krytyków na stronie Rotten Tomatoes. Znajdują się tutaj wizualizacje informacji zawartych w tym zbiorze, a także oceny modeli zbudowanych w oparciu o dane ze zbioru. Użytkownik ma również możliwość przetestowania działania modeli na dwa sposoby:
        <div class="list-item">- może wprowadzić własną recenzję i zobaczyć przewidywany sentyment</div>
        <div class="list-item">- może podać link do recenzji konkretnego filmu/serialu ze strony Rotten Tomatoes i zobaczyć jaki sentyment przewiduje dla nich model.</div>
    </div>
''', unsafe_allow_html=True)
