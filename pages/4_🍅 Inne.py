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

# Inicjalizacja zasobów NLTK
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

# Funkcja czyszcząca tekst
def clean_text(text):
    text = text.lower()  # zamiana wszystkich liter na małe
    text = ''.join([char for char in text if char not in string.punctuation])  # usunięcie znaków interpunkcyjnych
    tokens = word_tokenize(text)  # tokenizacja
    tokens = [word for word in tokens if word not in stop_words]  # usunięcie stopwords
    return ' '.join(tokens)  # połączenie tokenów

# Wczytanie modelu i wektoryzera
model = joblib.load("naive_bayes_model.pkl") 
vectorizer = joblib.load("vectorizer.pkl")  

# Nowa funkcja do pobierania recenzji bez Selenium
def scrape_reviews(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Dopasuj do struktury HTML Rotten Tomatoes
        reviews_elements = soup.find_all(class_='review-text')
        reviews = [review.get_text() for review in reviews_elements]
        return reviews
    else:
        st.write("Nie udało się pobrać strony. Sprawdź URL.")
        return []

# Funkcja do przewidywania sentymentu
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
                st.write(f"Predicted Sentiment: {'Positive' if sentiments[i] == 2 else 'Negative' if sentiments[i] == 0 else 'Neutral'}")
                st.write("---")
        else:
            st.write("No reviews found on this page.")
