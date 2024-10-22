import streamlit as st
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px


st.markdown(
    """
    <style>
    .emoji-top {
        margin-top: -20px; /* Zmniejszenie marginesu górnego */
    }
    </style>
    
    <div style="text-align: left;">
        <h1>🍅 Ocena modeli</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

# Przykładowe dane (w rzeczywistości wczytaj swoje dane)
data = {
    'sentiment': ['positive', 'negative', 'positive', 'negative', 'neutral', 'positive', 'negative'],
    'predicted': ['positive', 'negative', 'neutral', 'positive', 'negative', 'positive', 'negative'],
}

# Tworzenie DataFrame
df = pd.DataFrame(data)

# Funkcja do wyświetlania metryk
def show_metrics(y_true, y_pred):
    report = classification_report(y_true, y_pred, output_dict=True)
    metrics_df = pd.DataFrame(report).transpose()
    return metrics_df

# Ocena modelu
metrics_df = show_metrics(df['sentiment'], df['predicted'])

# Nagłówek
st.title('Ocena Modelu Analizy Sentymentu')
st.write('Wyniki klasyfikacji modelu analizy sentymentu za pomocą klasyfikatora Bayesa')

# Wyświetlanie metryk
st.subheader('Metryki Modelu')
st.dataframe(metrics_df[['precision', 'recall', 'f1-score', 'support']])

# Wykres słupkowy metryk
st.subheader('Wykres Słupkowy Metryk')
metrics_df[['precision', 'recall', 'f1-score']].plot(kind='bar', figsize=(10, 6))
plt.title('Metryki Modelu')
plt.xlabel('Klasa')
plt.ylabel('Wartość')
plt.xticks(rotation=45)
st.pyplot(plt)

# Macierz pomyłek
st.subheader('Macierz Pomyłek')
cm = confusion_matrix(df['sentiment'], df['predicted'])
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['positive', 'negative', 'neutral'], yticklabels=['positive', 'negative', 'neutral'])
plt.xlabel('Przewidywane')
plt.ylabel('Rzeczywiste')
plt.title('Macierz Pomyłek')
st.pyplot(fig)

# Dodatkowe wizualizacje
st.subheader('Rozkład Sentymentów')
df['sentiment'].value_counts().plot(kind='pie', autopct='%1.1f%%', figsize=(8, 6))
plt.title('Rozkład Sentymentów')
st.pyplot(plt)


