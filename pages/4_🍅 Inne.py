import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = st.text_input("Podaj link do recenzji na RT :",)

if url:
    res = requests.get(url)
    
    if res.status_code == 200:
        content = BeautifulSoup(res.content, 'html.parser')

        title_tag = content.find('a', class_='sidebar-title')
        title = title_tag.get_text(strip=True) if title_tag else "Nie znaleziono tytułu"
        
        image_tag = content.find('img', {'data-qa': 'sidebar-poster-img'}) 
        image_url = image_tag['src'] if image_tag else None
        
        st.write(f"**Tytuł:** {title}")
        col1, col2 = st.columns([1, 2])
        if image_url:
            col1.image(image_url, width=280)
        else:
            col1.write("Nie znaleziono obrazka.")
        
        reviews = content.find_all('p', class_='review-text')
        
        review_texts = [review.get_text(strip=True) for review in reviews]
        if review_texts:
            reviews_df = pd.DataFrame(review_texts, columns=['review_content'])
            col2.dataframe(reviews_df, use_container_width=True)
        else:
            st.write("Nie znaleziono recenzji na tej stronie.")
    else:
        st.write("Nie udało się pobrać strony. Sprawdź, czy adres URL jest poprawny.")

