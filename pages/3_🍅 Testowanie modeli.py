import streamlit as st
import numpy as np
import pandas as pd
import joblib
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from streamlit_option_menu import option_menu

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
nltk.download('punkt_tab')
stop_words = set(stopwords.words('english'))

st.markdown('######')

def clean_text(text):
    text = text.lower()  # zamiana na małe litery
    text = ''.join([char for char in text if char not in string.punctuation])  # usunięcie znaków interpunkcyjnych
    tokens = word_tokenize(text)  # tokenizacja
    tokens = [word for word in tokens if word not in stop_words]  # usunięcie stopwords
    return ' '.join(tokens)  # połączenie tokenów w jeden tekst

def predict_sentiment(reviews):
    cleaned_reviews = [clean_text(review) for review in reviews]
    features = vectorizer.transform(cleaned_reviews)
    predictions = model.predict(features)
    return predictions

selected = option_menu(
    menu_title=None,  
    options=["Naiwny klasyfikator Bayesa", "Regresja logistyczna"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal", 
)

if selected=="Naiwny klasyfikator Bayesa":

    st.markdown('######')

    model = joblib.load("naive_bayes_model.pkl") 
    vectorizer = joblib.load("vectorizer.pkl")  

    st.markdown("### Analiza sentymentu dla recenzji użytkowników")

    user_review = st.text_area("Wprowadź swoją recenzję tutaj :",)

    if st.button('Analizuj recenzję'):
        if user_review:
            with st.spinner('Analizowanie recenzji...'):
                reviews = [user_review]  
                sentiments = predict_sentiment(reviews)  

                st.write(f"**Twoja recenzja :** {user_review}")
                st.write(f"Przewidywany sentyment : {'Pozytywny' if sentiments[0] == 2 else 'Negatywny' if sentiments[0] == 0 else 'Neutralny'}")
        else:
            st.write("Proszę wprowadzić recenzję.")


if selected=="Regresja logistyczna":

    st.markdown('######')

    model = joblib.load("logistic_regression_model.pkl") 
    vectorizer = joblib.load("vectorizer.pkl")  

    st.markdown("### Analiza sentymentu dla recenzji użytkowników")

    user_review = st.text_area("Wprowadź swoją recenzję tutaj :",)

    if st.button('Analizuj recenzję'):
        if user_review:
            with st.spinner('Analizowanie recenzji...'):
                reviews = [user_review]  
                sentiments = predict_sentiment(reviews)  

                st.write(f"**Twoja recenzja :** {user_review}")
                st.write(f"Przewidywany sentyment : {'Pozytywny' if sentiments[0] == 2 else 'Negatywny' if sentiments[0] == 0 else 'Neutralny'}")
        else:
            st.write("Proszę wprowadzić recenzję.")



    
