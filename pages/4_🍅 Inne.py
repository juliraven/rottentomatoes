import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = st.text_input("Podaj link do recenzji na RT", "https://www.rottentomatoes.com/m/terrifier_3/reviews")

# Sprawdzamy, czy użytkownik wprowadził URL
if url:
    # Wysłanie żądania HTTP do podanego URL
    res = requests.get(url)
    
    # Sprawdzenie, czy odpowiedź jest poprawna
    if res.status_code == 200:
        # Przetworzenie zawartości strony za pomocą BeautifulSoup
        content = BeautifulSoup(res.content, 'html.parser')
        
        # Wyszukanie recenzji
        reviews = content.find_all('div', class='review-text')
        
        # Wyodrębnienie tekstu recenzji
        review_texts = [review.get_text(strip=True) for review in reviews]
        
        # Sprawdzenie, czy recenzje zostały znalezione
        if review_texts:
            st.write(f"Znaleziono {len(review_texts)} recenzji:")
            for i, review in enumerate(review_texts, start=1):
                st.write(f"**Recenzja {i}:** {review}")
                st.write("---")  # Separator między recenzjami
        else:
            st.write("Nie znaleziono recenzji na tej stronie.")
    else:
        st.write("Nie udało się pobrać strony. Sprawdź, czy adres URL jest poprawny.")
