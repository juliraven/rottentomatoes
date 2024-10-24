import streamlit as st
import numpy as np
import pandas as pd
import joblib
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


st.markdown(
    """
    <style>
    .emoji-top {
        margin-top: -20px; /* Zmniejszenie marginesu górnego */
    }
    </style>
    
    <div style="text-align: left;">
        <h1>🍅 Testowanie modeli</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

# Funkcja do pobierania recenzji
def scrape_reviews(url):
    # Ustawienia Selenium z automatycznym pobraniem Edge WebDriver
    edge_options = Options()
    # Możesz dodać różne opcje, np. edge_options.add_argument('--headless') jeśli chcesz uruchomić w trybie bezgłowym

    # Inicjalizacja WebDriver
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)
    
    driver.get(url)

    try:
        # Oczekiwanie na załadowanie elementów recenzji
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "review-text"))
        )

        # Znajdź wszystkie elementy zawierające recenzje
        reviews_elements = driver.find_elements(By.CLASS_NAME, "review-text")

        # Pobierz tekst recenzji
        reviews = [review.text for review in reviews_elements]

        return reviews

    except Exception as e:
        st.error(f"Wystąpił błąd: {str(e)}")
        return []

    finally:
        # Zakończ działanie przeglądarki
        driver.quit()

# Interfejs użytkownika w Streamlit
st.title("Scraping Rotten Tomatoes Reviews")

# Formularz do wprowadzenia linku przez użytkownika
url = st.text_input("Wprowadź URL strony z recenzjami Rotten Tomatoes", 
                    "https://www.rottentomatoes.com/m/terrifier_3/reviews")

# Przycisk do pobrania recenzji
if st.button('Pobierz recenzje'):
    with st.spinner('Pobieranie recenzji...'):
        reviews = scrape_reviews(url)  # Pobierz recenzje
        if reviews:
            st.write(f"Znaleziono {len(reviews)} recenzji:")
            for i, review in enumerate(reviews, start=1):
                st.write(f"**Recenzja {i}:** {review}")
        else:
            st.write("Nie znaleziono recenzji na stronie.")
