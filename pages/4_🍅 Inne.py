import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = st.text_input("Podaj link do recenzji na RT", "https://www.rottentomatoes.com/m/terrifier_3/reviews")

res = requests.get(url)

content = BeautifulSoup(res.content, 'html.parser')
st.code(content)
