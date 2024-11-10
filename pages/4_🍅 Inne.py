import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = st.text_input("Podaj link do recenzji na RT :",)

if url:
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
