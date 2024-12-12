import streamlit as st
import numpy as np
import pandas as pd
import joblib
import nltk
import string
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
    st.markdown('######')

    url = st.text_input("Podaj link do recenzji na RT:")

    if url:
        res = requests.get(url)

        if res.status_code == 200:
            content = BeautifulSoup(res.content, 'html.parser')

            title_tag = content.find('a', class_='sidebar-title')
            title = title_tag.get_text(strip=True) if title_tag else "Nie znaleziono tytułu"
            
            image_tag = content.find('rt-img', {'data-qa': 'sidebar-poster-img'})
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
                for review in review_texts:
                    st.write(f"**Recenzja:**\n{review}")
                    st.markdown("---") 

                sentiments = predict_sentiment(review_texts)
                for i, sentiment in enumerate(sentiments):
                    sentiment_label = "Pozytywny" if sentiment == 1 else "Negatywny"
                    sentiment_color = "green" if sentiment == 1 else "red"
                    st.markdown(f"<h3>Przewidywany sentyment dla recenzji {i+1}: <span style='color: {sentiment_color};'>{sentiment_label}</span></h3>", unsafe_allow_html=True)
            else:
                st.write("Nie znaleziono recenzji na tej stronie.")
        else:
            st.write("Nie udało się pobrać strony. Sprawdź, czy adres URL jest poprawny.")


    
if selected == "Sieć neuronowa":
    
    url = st.text_input("Podaj link do recenzji na RT:")

    if url:
        res = requests.get(url)
    
        if res.status_code == 200:
            content = BeautifulSoup(res.content, 'html.parser')

            title_tag = content.find('a', class_='sidebar-title')
            title = title_tag.get_text(strip=True) if title_tag else "Nie znaleziono tytułu"
        
            image_tag = content.find('rt-img', {'data-qa': 'sidebar-poster-img'}) 
            image_url = image_tag['src'] if image_tag else None
        
            col1, col2 = st.columns([1, 2])
            if image_url:
                col1.write(f"**Tytuł:** {title}")
                col1.image(image_url, width=280)
            else:
                col1.write("Nie znaleziono obrazka.")
        
            reviews = content.find_all('p', class_='review-text')
        
            review_texts = [review.get_text(strip=True) for review in reviews]
            if review_texts:
                for review in review_texts:
                    st.write(f"**Recenzja:**\n{review}")
                    st.markdown("---")
            else:
                st.write("Nie znaleziono recenzji na tej stronie.")
        else:
            st.write("Nie udało się pobrać strony. Sprawdź, czy adres URL jest poprawny.")













