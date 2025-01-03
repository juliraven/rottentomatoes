import streamlit as st
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu

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

st.markdown('######')

selected = option_menu(
    menu_title=None,  
    options=["Wykresy", "Ranking filmów"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal", 
)

if selected == "Wykresy":
    st.sidebar.empty() 

    st.markdown('######')
    
    st.markdown('### Chmury słów dla recenzji o danym sentymencie')
    c1, c2 = st.columns((3,3))
    c1.image("negatywne.png", caption="Chmura słów dla recenzji o negatywnym sentymencie")
    c2.image("pozytywne.png", caption="Chmura słów dla recenzji o pozytywnym sentymencie")

    st.markdown('######')
    st.markdown('### Rozkład liczby recenzji w czasie w podziale na sentyment')

    dane = pd.read_csv('dane_c.csv')

    colors = {0: 'indianred', 1: 'lightgreen'}

    fig = go.Figure()

    for sentiment in dane['sentiment'].unique():
        sentiment_data = dane[dane['sentiment'] == sentiment]
        fig.add_trace(go.Bar(
        x=sentiment_data['rok'],
        y=sentiment_data['count'],
        name=f'{sentiment}',
        marker_color=colors[sentiment] 
        ))

    fig.update_layout(
    barmode='group',  
    xaxis_title='Rok',
    yaxis_title='Liczba recenzji',
    legend_title='Sentiment',
    template='plotly',
    margin=dict(t=20),
    plot_bgcolor='rgba(0, 0, 0, 0)',  
    paper_bgcolor='rgba(0, 0, 0, 0)'
    )

    fig.update_layout(
    xaxis=dict(
        tickmode='linear', 
        tick0=2000,        
        dtick=1,           
        tickformat='d'     
    ))

    st.plotly_chart(fig)
    
    st.markdown('######')
    dane1 = pd.read_csv('dane_g.csv')
    gatunki = dane1['genres'].unique()
    wybierz_gatunek = st.selectbox('Wybierz gatunek :', gatunki)
    filtered_df = dane1[dane1['genres'] == wybierz_gatunek]

    custom_colors2 = ['indianred', 'lightgreen'] 

    fig2 = px.pie(filtered_df, values='count', names='sentiment', color='sentiment',
             width=800,  
             height=500,
             color_discrete_sequence=custom_colors2)

    fig2.update_traces(textfont_size=20)
    fig2.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',  
                      paper_bgcolor='rgba(0, 0, 0, 0)')
    st.markdown('### Podział recenzji wg sentymentu dla wybranego gatunku')
    st.plotly_chart(fig2, use_container_width=True)


elif selected == "Ranking filmów":
    st.markdown('######')
    st.markdown('### Ranking filmów')

    df = pd.read_csv('dane_r.csv')
    df['original_release_date'] = pd.to_datetime(df['original_release_date'])
    df['original_release_date'] = df['original_release_date'].dt.year
    df['original_release_date'] = df['original_release_date'].astype(int)
    
    st.sidebar.header('Opcje filtrowania')

    date_filter = st.sidebar.slider(
    'Wybierz rok premiery :',
    min_value=df['original_release_date'].min(),
    max_value=df['original_release_date'].max(),
    value=(df['original_release_date'].min(), df['original_release_date'].max())
    )

    tomatometer_filter = st.sidebar.slider('Wybierz ocenę krytyków (Tomatometer) :', 
                                       int(df['tomatometer_rating'].min()), 
                                       int(df['tomatometer_rating'].max()), 
                                       (int(df['tomatometer_rating'].min()), int(df['tomatometer_rating'].max())))


    audience_filter = st.sidebar.slider('Wybierz ocenę widowni :', 
                                    int(df['audience_rating'].min()), 
                                    int(df['audience_rating'].max()), 
                                    (int(df['audience_rating'].min()), int(df['audience_rating'].max())))

    sentiment_filter = st.sidebar.multiselect('Wybierz sentyment :', options=df['sentiment'].unique(), default=df['sentiment'].unique())


    filtered_df = df[
    (df['original_release_date'].between(date_filter[0], date_filter[1])) &
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
    'original_release_date': 'Rok premiery',
    'tomatometer_rating': 'Ocena krytyków',
    'audience_rating': 'Ocena widowni'})
    sorted_df = sorted_df.dropna(subset=['Ocena krytyków', 'Ocena widowni'])
    sorted_df['Ocena krytyków'] = sorted_df['Ocena krytyków'].round(2)
    sorted_df['Ocena widowni'] = sorted_df['Ocena widowni'].round(2)
    
    max_tomatometer = sorted_df['Ocena krytyków'].max()
    max_audience = sorted_df['Ocena widowni'].max()

    def create_bar(value, max_value, color):
        bar_length = (value / max_value) * 100 
        return f"<div style='width: 100%; background-color: #e0e0e0;'><div style='width: {bar_length}%; background-color: {color}; height: 10px;'></div></div>"

    html_table = "<table style='width:100%; border-collapse: collapse; background-color: rgba(105, 105, 105, 0.8); color: white;'>"
    html_table += "<tr><th>Tytuł filmu</th><th>Rok premiery</th><th>Ocena krytyków</th><th>Ocena widowni</th><th>Tomatometer</th><th>Audience</th></tr>"

    for index, row in sorted_df.iterrows():
        tomatometer_bar = create_bar(row['Ocena krytyków'], max_tomatometer, 'magenta')
        audience_bar = create_bar(row['Ocena widowni'], max_audience, 'blue')
        html_table += f"<tr><td>{row['Tytuł filmu']}</td><td>{row['Rok premiery']}</td><td>{row['Ocena krytyków']}</td><td>{row['Ocena widowni']}</td><td>{tomatometer_bar}</td><td>{audience_bar}</td></tr>"

    html_table += "</table>"

    st.markdown(html_table, unsafe_allow_html=True)

   












