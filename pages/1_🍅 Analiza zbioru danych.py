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
        <h1>🍅 Analiza zbioru danych</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown('###')

tab1, tab2, tab3 = st.tabs(["Wykresy", "Ranking", "Liczba recenzji w czasie"])

with tab1:
    dane1 = pd.read_csv('dane1.csv')
    dane2 = pd.read_csv('dane2.csv')
    dane3 = pd.read_csv('dane3.csv')
    dane4 = pd.read_csv('dane4.csv')
    
    st.markdown('### Chmury słów dla recenzji o danym sentymencie')
    c1, c2, c3 = st.columns((2,2,2))
    c1.image("negatywne.png", caption="Chmura słów dla recenzji o negatywnym sentymencie")
    c2.image("pozytywne.png", caption="Chmura słów dla recenzji o pozytywnym sentymencie")
    c3.image("neutralne.png", caption="Chmura słów dla recenzji o neutralnym sentymencie")

    st.markdown('###')

    a1, a2 = st.columns((2,2))
    sentiment_counts = dane1['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']

    custom_colors = ['forestgreen', 'indianred', 'deepskyblue']  

    fig = px.pie(sentiment_counts, 
             values='count', 
             names='sentiment', 
             width=800,  
             height=500,
             color_discrete_sequence=custom_colors)

    fig.update_traces(textfont_size=20)
    a1.markdown('### Podział recenzji wg sentymentu')
    a1.plotly_chart(fig, use_container_width=True)

    custom_colors1 = ['red', 'rgb(61,94,47)']  

    fig1 = px.pie(dane4, 
             values='review_type', 
             names='index', 
             width=800,  
             height=500,
             color_discrete_sequence=custom_colors1)

    fig1.update_traces(textfont_size=20)
    a2.markdown('### Podział recenzji wg typu')
    a2.plotly_chart(fig1, use_container_width=True)
    st.markdown('###')

    gatunki = dane2['genres'].unique()
    wybierz_gatunek = st.selectbox('Wybierz gatunek :', gatunki)
    filtered_df = dane2[dane2['genres'] == wybierz_gatunek]
    filtered_df1 = dane3[dane3['genres'] == wybierz_gatunek]
    b1, b2 = st.columns((2,2))

    custom_colors2 = ['indianred', 'deepskyblue', 'forestgreen'] 

    fig2 = px.pie(filtered_df1, values='count', names='sentiment', color='sentiment',
             width=800,  
             height=500,
             color_discrete_sequence=custom_colors2)

    fig2.update_traces(textfont_size=20)
    b1.markdown('### Podział recenzji wg sentymentu dla wybranego gatunku')
    b1.plotly_chart(fig2, use_container_width=True)

    fig3 = px.pie(filtered_df, values='count', names='review_type', color='review_type',
             width=800,  
             height=500,
             color_discrete_sequence=custom_colors1)

    fig3.update_traces(textfont_size=20)
    b2.markdown('### Podział recenzji wg typu dla wybranego gatunku')
    b2.plotly_chart(fig3, use_container_width=True)



tab2.markdown('### Ranking filmów')
    
def load_data(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    df = pd.concat([df1, df2], ignore_index=True)
    return df

file1 = 'dane5_1.csv'
file2 = 'dane5_2.csv'


df = load_data(file1, file2)
df['original_release_date'] = pd.to_datetime(df['original_release_date'])

with tab2 :
    st.sidebar.header('Opcje filtrowania')

date_filter = tab2.sidebar.slider(
    'Wybierz zakres dat (rok premiery) :',
    min_value=df['original_release_date'].min().date(),
    max_value=df['original_release_date'].max().date(),
    value=(df['original_release_date'].min().date(), df['original_release_date'].max().date())
)

tomatometer_filter = tab2.sidebar.slider('Wybierz ocenę krytyków (Tomatometer) :', 
                                       int(df['tomatometer_rating'].min()), 
                                       int(df['tomatometer_rating'].max()), 
                                       (int(df['tomatometer_rating'].min()), int(df['tomatometer_rating'].max())))


audience_filter = tab2.sidebar.slider('Wybierz ocenę widowni :', 
                                    int(df['audience_rating'].min()), 
                                    int(df['audience_rating'].max()), 
                                    (int(df['audience_rating'].min()), int(df['audience_rating'].max())))

sentiment_filter = tab2.sidebar.multiselect('Wybierz sentyment :', options=df['sentiment'].unique(), default=df['sentiment'].unique())


filtered_df = df[(df['original_release_date'].between(pd.to_datetime(date_filter[0]), pd.to_datetime(date_filter[1]))) &
                 (df['tomatometer_rating'].between(tomatometer_filter[0], tomatometer_filter[1])) &
                 (df['audience_rating'].between(audience_filter[0], audience_filter[1])) &
                 (df['sentiment'].isin(sentiment_filter))]


aggregated_df = filtered_df.groupby('movie_title').agg(
    {
        'original_release_date': 'first',  # Zachowujemy datę premiery
        'tomatometer_rating': 'mean',       # Średnia ocena krytyków
        'audience_rating': 'mean'         # Średnia ocena widowni
    }).reset_index()


sorted_df = aggregated_df.sort_values(by=['audience_rating', 'tomatometer_rating'], ascending=False)
sorted_df['original_release_date']=sorted_df['original_release_date'].astype(str).str[:10]
sorted_df = sorted_df.rename(columns={
    'movie_title': 'Tytuł filmu',
    'original_release_date': 'Data premiery',
    'tomatometer_rating': 'Ocena krytyków',
    'audience_rating': 'Ocena widowni'})
    
max_tomatometer = sorted_df['Ocena krytyków'].max()
max_audience = sorted_df['Ocena widowni'].max()

def create_bar(value, max_value, color):
    bar_length = (value / max_value) * 100 
    return f"<div style='width: 100%; background-color: #e0e0e0;'><div style='width: {bar_length}%; background-color: {color}; height: 10px;'></div></div>"

html_table = "<table style='width:100%; border-collapse: collapse;'>"
html_table += "<tr><th>Tytuł filmu</th><th>Data Premiery</th><th>Ocena krytyków</th><th>Ocena widowni</th><th>Tomatometer</th><th>Audience</th></tr>"

for index, row in sorted_df.iterrows():
    tomatometer_bar = create_bar(row['Ocena krytyków'], max_tomatometer, 'magenta')
    audience_bar = create_bar(row['Ocena widowni'], max_audience, 'blue')
    html_table += f"<tr><td>{row['Tytuł filmu']}</td><td>{row['Data premiery']}</td><td>{row['Ocena krytyków']}</td><td>{row['Ocena widowni']}</td><td>{tomatometer_bar}</td><td>{audience_bar}</td></tr>"

html_table += "</table>"

tab2.markdown(html_table, unsafe_allow_html=True)





