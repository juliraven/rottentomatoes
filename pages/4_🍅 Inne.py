import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = st.text_input("Podaj link do recenzji na RT :",)

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = st.text_input("Podaj link do recenzji na Rotten Tomatoes",)

if url:
    res = requests.get(url)
    
    if res.status_code == 200:
        content = BeautifulSoup(res.content, 'html.parser')

        title_tag = content.find('a', class_='sidebar-title')
        title = title_tag.get_text(strip=True) if title_tag else "Nie znaleziono tytułu"
        
        image_tag = content.find('a', href_='img src')
        image_url = image_tag['img src'] if image_tag else None
        
        st.write(f"**Tytuł:** {title}")
        if image_url:
            st.image(image_url, caption="Obrazek", use_column_width=True)
        else:
            st.write("Nie znaleziono obrazka.")
        
        reviews = content.find_all('p', class_='review-text')
        
        review_texts = [review.get_text(strip=True) for review in reviews]
        if review_texts:
            reviews_df = pd.DataFrame(review_texts, columns=['review_content'])
            st.dataframe(reviews_df)
        else:
            st.write("Nie znaleziono recenzji na tej stronie.")
    else:
        st.write("Nie udało się pobrać strony. Sprawdź, czy adres URL jest poprawny.")

