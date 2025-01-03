import streamlit as st
import numpy as np
import pandas as pd
import joblib
import nltk
import string
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from streamlit_option_menu import option_menu
from PIL import Image
from nltk.stem import WordNetLemmatizer
import re
import emoji
from langdetect import detect
from nltk.corpus import wordnet
from nltk import pos_tag
import requests
from bs4 import BeautifulSoup
from keras.preprocessing.sequence import pad_sequences
import gdown
import tensorflow as tf

st.markdown(
    """
    <style>
    .emoji-top {
        margin-top: -20px; /* Zmniejszenie marginesu górnego */
    }
    </style>
    
    <div style="text-align: left;">
        <h1>🍅 Analiza sentymentu dla recenzji z Rotten Tomatoes</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown('######')

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Lematyzator :
lemmatizer = WordNetLemmatizer()

# Zdefiniowanie wyrazów funkcyjnych do usunięcia :
stop_words = set(stopwords.words('english')) - set([
    'against', 'not', 'no', 'don', "don't", 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
    'haven', "haven't", 'isn', "isn't", 'mightn', "mightn't", 'mustn', "mustn't",
    'needn', "needn't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",
    'won', "won't", 'wouldn', "wouldn't"
])

# Słownik powszechnych skrótów :
sk = {
    "aren't": "are not", "can't": "cannot", "couldn't": "could not", "didn't": "did not",
    "doesn't": "does not", "don't": "do not", "isn't": "is not", "shouldn't": "should not",
    "won't": "will not", "wouldn't": "would not", "'ve": "have", "'s": "own",
    "'m": "am", "'re": "are", "'ll":"will", "I'm": "I am", "you're": "you are", "he's": "he is",
    "she's": "she is", "it's": "it is", "they're": "they are", "we're": "we are",
    "I'll":"I will", "you'll": "you will", "she'll": "she will", "he'll": "he will", "it'll": "it will", 
    "they'll": "they will", "we'll": "we will", "I've":"I have", "you've": "you have", 
    "they've": "they have", "we've": "we have", "gonna": "going to", "gimme": "give me", "gonna": "going to",
    "'cause'": "because", "what's": "what is", "how's": "how has", "y'all": "you all",
    "ne'er": "never", "let's": "let us", "finna": "fixing to", "gotta": "got to", "'d": "would",
    "daresn't": "dare not", "dasn't": "dare not", "e'er": "ever", "everyone's": "everyone is"
}

# Funkcja rozwijająca skróty :
def expand_contractions(text, sk):
    return ' '.join([sk.get(word, word) for word in text.split()])

# Funkcja usuwająca html i url :
def remove_urls_and_html(text):
    return re.sub(r'http\S+|www\S+|<.*?>', '', text)

# Funkcja usuwająca zbędne znaki :
def remove_special_characters(text):
    text = re.sub(r'\[Full review in [^\]]+\]', '', text, flags=re.IGNORECASE) # usuwanie fraz "[Full review in ...]"
    text = re.sub(r'\d+', '', text)  # usuwanie liczb
    text = re.sub(f"[{string.punctuation}]", " ", text)  # usuwanie znaków interpunkcyjnych
    text = re.sub(r'\s+', ' ', text).strip()  # usuwanie zbędnych spacji
    text = re.sub(r'[^\w\s]', '', text)  # usuwanie znaków specjalnych
    return text

# Funkcja konwertująca emotikony na tekst :
def convert_emojis(text):
    return emoji.demojize(text)

# Funkcja usuwająca słowa z innych języków :
def remove_non_english_words(text):
    return ' '.join([word for word in text.split() if detect(word) == 'en'])

# Funkcja obsługująca negacje i tokenizację :
def tokenize_and_negate(text):
    tokens = word_tokenize(text)
    negated_tokens = []
    negation = False
    for i, token in enumerate(tokens):
        if token in {"not", "no", "never"}:
            negation = True
            negated_tokens.append(token)
        elif negation:
            if token not in stop_words:
                negated_tokens.append(token) 
            negation = False
        else:
            negated_tokens.append(token)
    return negated_tokens
    
# Funkcja mapująca POS : 
def get_wordnet_pos(tag):
    if tag.startswith('J'):  # przymiotniki
        return wordnet.ADJ
    elif tag.startswith('V'):  # czasowniki
        return wordnet.VERB
    elif tag.startswith('N'):  # rzeczowniki
        return wordnet.NOUN
    elif tag.startswith('R'):  # przysłówki
        return wordnet.ADV
    else:
        return None

# Funkcja obsługująca stopwords i lematyzację :
def remove_stopwords_and_lemmatize(tokens):
    tagged_tokens = pos_tag(tokens)  
    lemmatized_tokens = []
    for word, tag in tagged_tokens:
        wordnet_pos = get_wordnet_pos(tag) or wordnet.NOUN
        if word not in stop_words:
            lemmatized_tokens.append(lemmatizer.lemmatize(word, wordnet_pos))
    return lemmatized_tokens

# Funkcja czyszcząca :
def clean_text(text):
    text = text.lower()
    text = expand_contractions(text, sk)
    text = remove_urls_and_html(text)
    text = convert_emojis(text)
    text = remove_special_characters(text)
    tokens = tokenize_and_negate(text)
    tokens = remove_stopwords_and_lemmatize(tokens)
    return ' '.join(tokens)

def predict_sentiment(reviews):
    cleaned_reviews = [clean_text(review) for review in reviews]
    features = vectorizer.transform(cleaned_reviews)
    predictions = model.predict(features)
    return predictions

selected = option_menu(
    menu_title=None,  
    options=["Naiwny klasyfikator Bayesa", "Sieć neuronowa"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal", 
)

if selected == "Naiwny klasyfikator Bayesa":
    
    model = joblib.load("naive_bayes_model.pkl") 
    vectorizer = joblib.load("vectorizer.pkl") 

    links = [
    "https://www.rottentomatoes.com/tv/arcane_league_of_legends/s02/reviews",
    "https://www.rottentomatoes.com/tv/stranger_things/s04/reviews",
    "https://www.rottentomatoes.com/tv/the_witcher/s02/reviews",
    "https://www.rottentomatoes.com/m/terrifier_3/reviews"
    ] + ["własny link"]

    c1, c2 = st.columns([1.5, 0.5])

    with c1:
        url_choice = st.selectbox("Podaj link do recenzji z https://www.rottentomatoes.com/ lub wybierz jeden z dostępnych:", links)

        if url_choice == "własny link":
            url = st.text_input("Podaj własny link do recenzji na RT:")
        else:
            url = url_choice

    with c2:
        number = st.number_input("Wybierz liczbę recenzji do pobrania:", min_value=1, max_value=10, value=5, step=1)

    if url:
        res = requests.get(url)

        if res.status_code == 200:
            content = BeautifulSoup(res.content, 'html.parser')

            title_tag = content.find('a', class_='sidebar-title')
            title = title_tag.get_text(strip=True) if title_tag else "Nie znaleziono tytułu"
            
            image_tag = content.find('rt-img', {'data-qa': 'sidebar-poster-img'})
            image_url = image_tag['src'] if image_tag else None

            col1, col2, col3, col4 = st.columns([2, 2, 2, 2], gap="small") 

            with col2:
                if image_url:
                    st.image(image_url, width=200)
                else:
                    st.markdown("<div style='text-align: center;'>Nie znaleziono obrazka.</div>", unsafe_allow_html=True) 

            with col3:
                st.markdown(f"**Tytuł:** {title}") 

                if "https://www.rottentomatoes.com/m/" in url.lower():
                    details_selector = 'sidebar-movie-details'
                elif "https://www.rottentomatoes.com/tv/" in url.lower():
                    details_selector = 'sidebar-tv-details'
                else:
                    None
                    
                if details_selector:
                    info = content.find('ul', {'data-qa': details_selector})
                    
                    if info:
                        details = [detail.get_text(strip=True) for detail in info.find_all('li')]
                        st.write("**Szczegóły:**")
                        for detail in details:
                            st.write(f"- {detail}")
                    else:
                        st.write(f"Nie znaleziono szczegółów dla {details_selector}.")
                else:
                    st.write("Nie rozpoznano typu strony (film/TV).")

            reviews = content.find_all('p', class_='review-text')
            review_texts = [review.get_text(strip=True) for review in reviews[:number]]

            if review_texts:
                for i, review in enumerate(review_texts):
                    sentiments = predict_sentiment([review])

                    sentiment_label = "Pozytywny" if sentiments[0] == 1 else "Negatywny"
                    sentiment_color = "green" if sentiments[0] == 1 else "red"

                    st.markdown(f"""
                    <div style="background-color:  #390808; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                        <h4>Recenzja {i + 1}:</h4>
                        <p>{review}</p>
                        <h4>Przewidywany sentyment: <span style="color: {sentiment_color};">{sentiment_label}</span></h4>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("---")
            else:
                st.write("Nie znaleziono recenzji na tej stronie.")
        else:
            st.write("Nie udało się pobrać strony. Sprawdź, czy adres URL jest poprawny.")


    
if selected == "Sieć neuronowa":
    
     # Funkcja do pobierania plików z Google Drive :
    def download_from_gdrive(file_id, output_path):
        url = f"https://drive.google.com/uc?id={file_id}"
        if not os.path.exists(output_path):
            gdown.download(url, output_path, quiet=False)

    model_file_id = "1NGwus3PyhZRIgK-D3WyX6eCniJryUc3N"
    
    download_from_gdrive(model_file_id, "model3.keras")

    model = tf.keras.models.load_model("model3.keras")
    tokenizer = joblib.load("tokenizer3.pkl") 

    max_length = 30 

    st.markdown("""
    <style>
        .css-1v3fvcr {
            margin-top: 0px;
            margin-bottom: 0px;
        }
    </style>
    """, unsafe_allow_html=True)

    links = [
    "https://www.rottentomatoes.com/tv/arcane_league_of_legends/s02/reviews",
    "https://www.rottentomatoes.com/tv/stranger_things/s04/reviews",
    "https://www.rottentomatoes.com/tv/the_witcher/s02/reviews",
    "https://www.rottentomatoes.com/m/terrifier_3/reviews"
    ] + ["własny link"]

    c1, c2 = st.columns([1.5, 0.5])

    with c1:
        url_choice = st.selectbox("Podaj link do recenzji z https://www.rottentomatoes.com/ lub wybierz jeden z dostępnych:", links)

        if url_choice == "własny link":
            url = st.text_input("Podaj własny link do recenzji na RT:")
        else:
            url = url_choice

    with c2:
        number = st.number_input("Wybierz liczbę recenzji do pobrania:", min_value=1, max_value=10, value=5, step=1)

    if url:
        res = requests.get(url)

        if res.status_code == 200:
            content = BeautifulSoup(res.content, 'html.parser')

            title_tag = content.find('a', class_='sidebar-title')
            title = title_tag.get_text(strip=True) if title_tag else "Nie znaleziono tytułu"
            
            image_tag = content.find('rt-img', {'data-qa': 'sidebar-poster-img'})
            image_url = image_tag['src'] if image_tag else None

            col1, col2, col3, col4 = st.columns([2, 2, 2, 2], gap="small")

            with col2:
                if image_url:
                    st.image(image_url, width=200) 
                else:
                    st.write("Nie znaleziono obrazka.")

            with col3:
                st.markdown(f"**Tytuł:** {title}") 

                if "https://www.rottentomatoes.com/m/" in url.lower():
                    details_selector = 'sidebar-movie-details'
                elif "https://www.rottentomatoes.com/tv/" in url.lower():
                    details_selector = 'sidebar-tv-details'
                else:
                    None

                if details_selector:
                    info = content.find('ul', {'data-qa': details_selector})
                    
                    if info:
                        details = [detail.get_text(strip=True) for detail in info.find_all('li')]
                        st.write("**Szczegóły:**")
                        for detail in details:
                            st.write(f"- {detail}")
                    else:
                        st.write(f"Nie znaleziono szczegółów dla {details_selector}.")
                else:
                    st.write("Nie rozpoznano typu strony (film/TV).")

            reviews = content.find_all('p', class_='review-text')
            review_texts = [review.get_text(strip=True) for review in reviews[:number]]

            if review_texts:
                for i, review in enumerate(review_texts):
                    cleaned_review = clean_text(review)
                    sequence = tokenizer.texts_to_sequences([cleaned_review])
                    padded_sequence = pad_sequences(sequence, maxlen=max_length)
                    prediction = model.predict(padded_sequence)
                    sentiments = prediction.argmax(axis=-1)

                    sentiment_label = "Pozytywny" if sentiments[0] == 1 else "Negatywny"
                    sentiment_color = "green" if sentiments[0] == 1 else "red"

                    st.markdown(f"""
                    <div style="background-color:  #390808; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                        <h4>Recenzja {i + 1}:</h4>
                        <p>{review}</p>
                        <h4>Przewidywany sentyment: <span style="color: {sentiment_color};">{sentiment_label}</span></h4>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("---")
            else:
                st.write("Nie znaleziono recenzji na tej stronie.")
        else:
            st.write("Nie udało się pobrać strony. Sprawdź, czy adres URL jest poprawny.")

    
