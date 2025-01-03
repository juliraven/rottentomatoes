import streamlit as st

st.set_page_config(page_title="Analiza sentymentu", page_icon="🎥", layout="wide")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 57% 50%,rgba(139, 0, 0, 1), rgba(26, 101, 60, 1), rgba(235, 0, 0, 1));
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

st.markdown(
    """
    <style>
    /* Kontener dla ramki */
    .bordered-text-container {
        position: relative;
        border-radius: 0px; /* Zaokrąglenie rogów */
        overflow: hidden;
        margin: 20px 0; /* Margines wokół ramki */
        background-color: rgba(88, 7, 7, 0.2); /* Tło z przezroczystością */
        margin-top: -20px; /* Zmniejszenie odległości pomiędzy tytułem a ramką */
    }
    
    /* Tło w kontenerze z rozmyciem */
    .bordered-text-background {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(88, 7, 7, 0.2); /* Przezroczyste tło */
        filter: blur(100px); /* Rozmycie tła */
        z-index: -1; /* Tło za tekstem */
    }

    /* Właściwy kontener na tekst */
    .bordered-text {
        padding: 20px; /* Odstępy wewnętrzne */
        color: #ecdede; /* Kolor tekstu */
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

st.markdown('''
    <div class="bordered-text-container">
        <div class="bordered-text-background"></div>
        <div class="bordered-text">
            Strona ta poświęcona jest analizie sentymentu zbioru zawierającego recenzje filmów napisane przez krytyków na stronie Rotten Tomatoes. Znajdują się tutaj wizualizacje informacji zawartych w tym zbiorze, a także oceny modeli zbudowanych w oparciu o dane ze zbioru. Użytkownik ma również możliwość przetestowania działania modeli na dwa sposoby:
            <div class="list-item">- może wprowadzić własną recenzję i zobaczyć przewidywany sentyment</div>
            <div class="list-item">- może podać link do recenzji konkretnego filmu/serialu ze strony Rotten Tomatoes i zobaczyć jaki sentyment przewiduje dla nich model.</div>
        </div>
    </div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
