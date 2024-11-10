import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = st.text_input("Podaj link do recenzji na RT :",)

def extract_movie_title(url):
    try:
        if '/m/' in url:
            # Dla filmów
            title_part = url.split('/m/')[1].split('/reviews')[0]
            movie_title = title_part.replace('_', ' ').title()
            return movie_title
        elif '/tv/' in url:
            # Dla seriali
            parts = url.split('/tv/')[1].split('/')
            title_part = parts[0]
            season = parts[1] if len(parts) > 1 and parts[1].startswith('s') else None
            show_title = title_part.replace('_', ' ').title()
            
            # Jeśli sezon istnieje, dodaj go do tytułu
            if season:
                return f"{show_title} (Season {season[1:]})"
            else:
                return show_title
        else:
            return "Nieznany Tytuł"
    except IndexError:
        return "Nieznany Tytuł"

if url:
    movie_title, content_type = extract_movie_title_and_type(url)
    st.write(f"**Recenzje dla {content_type}:** {movie_title}")
    
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
