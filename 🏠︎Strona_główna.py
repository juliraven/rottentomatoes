import streamlit as st
from streamlit_extras.app_logo import add_logo

st.set_page_config(page_title="Analiza sentymentu", page_icon="🎥", layout="wide")

add_logo('logo.png', height=500)

st.sidebar.markdown(
    """
    <style>
        [data-testid="stSidebar"] img { /* Stylowanie logo jako obraz */
            margin: 0 auto
        }

        [data-testid="stSidebar"] {
            padding: 10px;
            font-family: sans-serif;
            font-size: 18px;
        }

        [data-testid="stSidebarNav"] {
            padding-top: 20px;  /* Odstęp, aby elementy nawigacyjne nie nachodziły na logo */
        }

    </style>
    """,
    unsafe_allow_html=True,
)



page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 59% 55%,rgba(139, 0, 0, 1), rgba(26, 101, 60, 1), rgba(235, 0, 0, 1));
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
        width: 350px;  /* Ustaw stałą szerokość */
        min-width: 350px;  /* Minimalna szerokość */
        max-width: 350px;  /* Maksymalna szerokość */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('######')

st.markdown(
    """
    <style>
    .bordered-text-container {
        position: relative;
        border-radius: 0px; /* Zaokrąglenie rogów */
        overflow: hidden;
        margin: 20px 0; /* Margines wokół ramki */
        background-color: rgba(88, 7, 7, 0.2); /* Tło z przezroczystością */
        margin-top: -20px; /* Zmniejszenie odległości pomiędzy tytułem a ramką */
    }
    
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

    .bordered-text {
        padding: 60px; /* Odstępy wewnętrzne */
        color: #ecdede; /* Kolor tekstu */
        font-size: 24px; /* Rozmiar czcionki */
        box-shadow: inset 0px 0px 5px rgba(0, 0, 0, 0.1); /* Wewnętrzny cień obramowania */
    }

    /* Stylowanie tylko listy wewnątrz kontenera .bordered-text */
    .bordered-text ul {
        list-style-type: disc; /* Kropki przy elementach listy */
        padding-left: 20px; /* Odstęp po lewej stronie listy */
    }

    .bordered-text li {
        font-size: 24px;
        color: #ecdede;
    }
    
    /* Ustalamy rozmiar czcionki tytułów w sidebarze, aby nie były wpływane */
    .sidebar .css-1d391kg {
        font-size: 16px;  /* Przywracamy rozmiar czcionki tytułów w sidebarze */
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
            <ul>
                <li>może wprowadzić własną recenzję i zobaczyć przewidywany sentyment</li>
                <li>może podać link do recenzji konkretnego filmu/serialu ze strony Rotten Tomatoes i zobaczyć jaki sentyment przewiduje dla nich model.</li>
            </ul>
        </div>
    </div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


