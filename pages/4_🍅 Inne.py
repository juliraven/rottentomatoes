import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = st.text_input("Podaj link do recenzji na RT :", "https://www.rottentomatoes.com/m/terrifier_3/reviews")

if url:
    res = requests.get(url)
    
    if res.status_code == 200:
        content = BeautifulSoup(res.content, 'html.parser')
    
        reviews = content.find_all('p', class_='review-text')
        
        review_texts = [review.get_text(strip=True) for review in reviews]
        
        if review_texts:
            reviews_df = pd.DataFrame(review_texts, columns=['review_content'])
            st.write(f"Znaleziono {len(review_texts)} recenzji:")
            st.dataframe(reviews_df)
        else:
            st.write("Nie znaleziono recenzji na tej stronie.")
    else:
        st.write("Nie udało się pobrać strony. Sprawdź, czy adres URL jest poprawny.")
