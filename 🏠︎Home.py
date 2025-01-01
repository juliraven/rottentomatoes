

import streamlit as st

st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #f7b42c, #fc575e); /* Tło w postaci gradientu */
        color: white;
        font-family: 'Arial', sans-serif;
        padding: 0;
        margin: 0;
    }
    [data-testid="stSidebar"] {
        width: 300px;  /* Ustaw stałą szerokość */
        min-width: 300px;  /* Minimalna szerokość */
        max-width: 300px;  /* Maksymalna szerokość */
    }
    .header {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-top: 50px;
    }
    .content {
        margin: 20px;
        font-size: 20px;
    }
    .highlight {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .section-title {
        font-size: 28px;
        font-weight: bold;
        margin-top: 20px;
    }
    .section-text {
        font-size: 22px;
        margin: 10px 0;
    }
    .button-style {
        padding: 10px 20px;
        background-color: #fc575e;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .button-style:hover {
        background-color: #f7b42c;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar content
st.sidebar.image('tomato.png', width=300)

# Main content
st.markdown('<div class="header">Analiza Sentymentu Recenzji Filmów</div>', unsafe_allow_html=True)
st.markdown('<div class="content">Strona ta poświęcona jest analizie sentymentu zbioru zawierającego recenzje filmów napisane przez krytyków na stronie Rotten Tomatoes. Znajdują się tutaj wizualizacje informacji zawartych w tym zbiorze, a także oceny modeli zbudowanych w oparciu o dane ze zbioru. Użytkownik ma również możliwość przetestowania działania modeli na dwa sposoby:</div>', unsafe_allow_html=True)

st.markdown('<div class="highlight">- może wprowadzić własną recenzję i zobaczyć przewidywany sentyment</div>', unsafe_allow_html=True)
st.markdown('<div class="highlight">- może podać link do recenzji konkretnego filmu/serialu ze strony Rotten Tomatoes i zobaczyć jaki sentyment przewiduje dla nich model.</div>', unsafe_allow_html=True)

# Call-to-action button
st.markdown('<button class="button-style">Przetestuj teraz!</button>', unsafe_allow_html=True)

