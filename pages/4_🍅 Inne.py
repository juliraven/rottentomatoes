import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = st.text_input("Podaj link do recenzji na RT :",)

def extract_movie_title(url):
    try:
        # Wyciągnij część między '/m/' a '/reviews'
        title_part = url.split('/m/')[1].split('/reviews')[0]
        # Zamień "_" na spacje i popraw format na tytułowy
        movie_title = title_part.replace('_', ' ').title()
        return movie_title
    except IndexError:
        return "Nieznany Tytuł"

if url:
    movie_title = extract_movie_title(url)
    st.write(f"**Tytuł filmu:** {movie_title}")
    res = requests.get(url)
    
    if res.status_code == 200:
        content = BeautifulSoup(res.content, 'html.parser')
    
        reviews = content.find_all('p', class_='review-text')
        
        review_texts = [review.get_text(strip=True) for review in reviews]
        
        if review_texts:
            st.write("Recenzje dla filmu")
            reviews_df = pd.DataFrame(review_texts, columns=['review_content'])
            st.dataframe(reviews_df, use_container_width=True)
        else:
            st.write("Nie znaleziono recenzji na tej stronie.")
    else:
        st.write("Nie udało się pobrać strony. Sprawdź, czy adres URL jest poprawny.")
