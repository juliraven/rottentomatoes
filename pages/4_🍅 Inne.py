import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.write("Podaj link")
url = st.text_input("Enter Rotten Tomatoes reviews page URL", "https://www.rottentomatoes.com/m/terrifier_3/reviews")


