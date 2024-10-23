import streamlit as st
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import joblib

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

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()  # zamiana wszystkich liter na małe
    text = ''.join([char for char in text if char not in string.punctuation])  # usunięcie znaków interpunkcyjnych
    tokens = word_tokenize(text)  # tokenizacja
    tokens = [word for word in tokens if word not in stop_words]  # usunięcie stopwords
    return ' '.join(tokens)  # połączenie tokenów

model = joblib.load("naive_bayes_model.pkl") 
vectorizer = joblib.load("vectorizer.pkl")  

# Funkcja do scrapowania recenzji ze strony Rotten Tomatoes
def scrape_reviews(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Znajdź wszystkie recenzje krytyków (dostosuj selektor do struktury Rotten Tomatoes)
    reviews_html = soup.find_all('div', class_='the_review')  # zmień selektor, jeśli potrzeba
    reviews = [review.get_text(strip=True) for review in reviews_html]
    
    return reviews

# Funkcja do przewidywania sentymentu dla recenzji
def predict_sentiment(reviews):
    cleaned_reviews = [clean_text(review) for review in reviews]
    features = vectorizer.transform(cleaned_reviews)
    predictions = model.predict(features)
    return predictions

# Interfejs użytkownika w Streamlit
st.title("Sentiment Analysis for Rotten Tomatoes Reviews")

# Formularz do wprowadzenia linku przez użytkownika
url = st.text_input("Enter Rotten Tomatoes reviews page URL", "https://www.rottentomatoes.com/m/terrifier_3/reviews")

# Po wprowadzeniu URL i kliknięciu przycisku pobierz recenzje
if st.button('Fetch and Analyze Reviews'):
    with st.spinner('Fetching reviews...'):
        reviews = scrape_reviews(url)  # pobierz recenzje
        if reviews:
            st.write(f"Found {len(reviews)} reviews")
            sentiments = predict_sentiment(reviews)  # przewiduj sentymenty

            # Wyświetl każdą recenzję z jej przewidywanym sentymentem
            for i, review in enumerate(reviews):
                st.write(f"**Review {i+1}:** {review}")
                st.write(f"Predicted Sentiment: {'Positive' if sentiments[i] == 1 else 'Negative' if sentiments[i] == -1 else 'Neutral'}")
                st.write("---")
        else:
            st.write("No reviews found on this page.")
