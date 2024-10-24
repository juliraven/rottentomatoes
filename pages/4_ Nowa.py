import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager, ChromeType  # Import dla Chromium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ustawienia Selenium z automatycznym pobraniem Chromium WebDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Ustaw na True, aby uruchomić w trybie headless

# Inicjalizacja WebDrivera Chromium
driver = webdriver.Chrome(
    service=Service(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    ),
    options=chrome_options,
)

def scrape_reviews(url):
    driver.get(url)
    reviews = []

    try:
        # Oczekiwanie na załadowanie elementów recenzji
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "review-text"))
        )

        # Znajdź wszystkie elementy zawierające recenzje
        reviews_elements = driver.find_elements(By.CLASS_NAME, "review-text")

        # Pobierz tekst recenzji
        reviews = [review.text for review in reviews_elements]

        # Sprawdź, czy recenzje zostały znalezione
        if not reviews:
            st.warning("Nie znaleziono recenzji na stronie.")
        else:
            for i, review in enumerate(reviews, start=1):
                st.write(f"Recenzja {i}: {review}")

    except Exception as e:
        st.error(f"Wystąpił błąd: {str(e)}")

# Ustawienia aplikacji Streamlit
st.title("Skrapowanie recenzji z Rotten Tomatoes")

# Wprowadzenie URL
url = st.text_input("Wprowadź URL do recenzji (np. https://www.rottentomatoes.com/m/terrifier_3/reviews):")

if st.button("Skrapuj"):
    if url:
        scrape_reviews(url)
    else:
        st.error("Proszę wprowadzić prawidłowy URL.")

# Zakończ działanie przeglądarki po zakończeniu działania aplikacji
driver.quit()


