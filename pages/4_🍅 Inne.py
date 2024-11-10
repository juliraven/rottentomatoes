import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = st.text_input("Podaj link do recenzji na RT", "https://www.rottentomatoes.com/m/terrifier_3/reviews")

res = requests.get(url)

content = BeautifulSoup(res.content, 'html.parser')

quotes = content.find_all('div', class_='review-text')
st.write(quotes)
