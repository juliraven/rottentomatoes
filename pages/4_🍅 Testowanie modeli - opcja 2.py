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
from streamlit_extras.app_logo import add_logo

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 57% 50%,rgba(94, 7, 7, 1), rgba(0, 0, 0, 1), rgba(128,33,33,1));
    background-blend-mode: multiply;
    background-size: cover;
    overflow: hidden; /* Prevent scrolling */
}

header[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

add_logo('logo.png', height=350)

st.sidebar.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            padding-top: 0px;
            padding: 10px;
            font-family: sans-serif;
            font-size: 18px;
        }

        [data-testid="stSidebarHeader"] {
            height: 20px;
            padding: 5px 10px; 
            margin: 0; 
            display: flex; 
            align-items: center;
            justify-content: center; 
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        width: 350px;  /* Ustaw stałą szerokość */
        min-width: 350px;  /* Minimalna szerokość */
        max-width: 350px;  /* Maksymalna szerokość */
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
sk = { "ain't": "is not","aren't": "are not","can't": "cannot","'cause": "because","could've": "could have","couldn't": "could not",
"daresn't": "dare not","dasn't": "dare not","didn't": "did not","doesn't": "does not","don't": "do not","e'er": "ever",
"everyone's": "everyone is","finna": "fixing to","gimme": "give me","gonna": "going to","gotta": "got to","hadn't": "had not",
"hasn't": "has not","haven't": "have not","he'd": "he would","he'll": "he will","he's": "he is","how'd": "how did","how'd'y": "how do you",
"how'll": "how will","how's": "how has","I'd": "I would","I'd've": "I would have","I'll": "I will","I'll've": "I will have",
"I'm": "I am","I've": "I have","isn't": "is not","it'd": "it would","it'd've": "it would have","it'll": "it will",
"it'll've": "it will have","it's": "it is","let's": "let us","ma'am": "madam","mayn't": "may not","might've": "might have",
"mightn't": "might not","mightn't've": "might not have","must've": "must have","mustn't": "must not","mustn't've": "must not have",
"needn't": "need not","needn't've": "need not have","ne'er": "never","o'clock": "of the clock","oughtn't": "ought not","oughtn't've": "ought not have",
"shan't": "shall not","shan't've": "shall not have","she'd": "she would","she'd've": "she would have","she'll": "she will",
"she'll've": "she will have","she's": "she is","should've": "should have","shouldn't": "should not","shouldn't've": "should not have",
"so's": "so as","so've": "so have","that'd": "that would","that'd've": "that would have","that's": "that is","there'd": "there would",
"there'd've": "there would have","there's": "there is","they'd": "they would","they'd've": "they would have","they'll": "they will",
"they'll've": "they will have","they're": "they are","they've": "they have","to've": "to have","wasn't": "was not","we'd": "we would",
"we'd've": "we would have","we'll": "we will","we'll've": "we will have","we're": "we are","we've": "we have","weren't": "were not",
"what'll": "what will","what'll've": "what will have","what're": "what are","what's": "what is","what've": "what have","when's": "when is",
"when've": "when have","where'd": "where did","where's": "where is","where've": "where have","who'll": "who will","who'll've": "who will have",
"who's": "who is","who've": "who have","why's": "why is","why've": "why have","will've": "will have","won't": "will not",
"won't've": "will not have","would've": "would have","wouldn't": "would not","wouldn't've": "would not have","y'all": "you all",
"y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",
"you'd": "you would","you'd've": "you would have","you'll": "you will","you'll've": "you will have","you're": "you are","you've": "you have"}


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

    links = ["własny link"] + [
    "https://www.rottentomatoes.com/tv/arcane_league_of_legends/s02/reviews",
    "https://www.rottentomatoes.com/tv/stranger_things/s04/reviews",
    "https://www.rottentomatoes.com/tv/the_witcher/s02/reviews",
    "https://www.rottentomatoes.com/m/terrifier_3/reviews"
    ]

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

                    sentiment_label = "pozytywny" if sentiments[0] == 1 else "negatywny"
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

    model_file_id = "1sg57qSrYzV9tSlpLP7Qox74DOrFzCGgJ"
    
    download_from_gdrive(model_file_id, "model_siec.keras")

    model = tf.keras.models.load_model("model_siec.keras")
    tokenizer = joblib.load("tokenizer.pkl") 

    max_length = 30 

    st.markdown("""
    <style>
        .css-1v3fvcr {
            margin-top: 0px;
            margin-bottom: 0px;
        }
    </style>
    """, unsafe_allow_html=True)

    links = ["własny link"] + [
    "https://www.rottentomatoes.com/tv/arcane_league_of_legends/s02/reviews",
    "https://www.rottentomatoes.com/tv/stranger_things/s04/reviews",
    "https://www.rottentomatoes.com/tv/the_witcher/s02/reviews",
    "https://www.rottentomatoes.com/m/terrifier_3/reviews"
    ]

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

                    sentiment_label = "pozytywny" if sentiments[0] == 1 else "negatywny"
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

    
