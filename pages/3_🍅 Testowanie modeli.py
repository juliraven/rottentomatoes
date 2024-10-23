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

def get_review_from_rotten_tomatoes(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        review_content = soup.find("div", class_="the_review").get_text(strip=True)
        return review_content
    except Exception as e:
        st.error(f"Error extracting review: {e}")
        return None

model = joblib.load("naive_bayes_model.pkl") 
vectorizer = joblib.load("vectorizer.pkl")  

st.sidebar.header("Menu")
option = st.sidebar.selectbox("Wybierz stronę", ["Predict Sentiment"])

if option == "Predict Sentiment":
    st.header("Predict the Sentiment of a Rotten Tomatoes Review")

    url = st.text_input("Enter the Rotten Tomatoes review URL:")

    if st.button("Predict Sentiment"):
        if url:
            review = get_review_from_rotten_tomatoes(url)
            if review:
                st.write("Original Review:")
                st.write(review)

                clean_review = clean_text(review)
                st.write("Cleaned Review:")
                st.write(clean_review)

                review_vector = vectorizer.transform([clean_review])
                sentiment = model.predict(review_vector)[0]

                st.write("Predicted Sentiment:")
                if sentiment == 2:
                    st.success("Positive")
                elif sentiment == 1:
                    st.info("Neutral")
                else:
                    st.error("Negative")
        else:
            st.error("Please enter a valid URL.")
