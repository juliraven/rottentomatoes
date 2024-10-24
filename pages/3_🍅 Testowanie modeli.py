import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Interfejs użytkownika w Streamlit
st.title("Pobieranie recenzji z Rotten Tomatoes")

# Przycisk do pobrania recenzji
if st.button('Pobierz recenzje'):
    with st.spinner('Pobieranie recenzji...'):
        # URL strony z recenzjami
        url = "https://www.rottentomatoes.com/m/terrifier_3/reviews"

        # Ustawienia Selenium z automatycznym pobraniem Chrome WebDriver
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Uruchom w trybie bezgłowym (opcjonalnie)
        chrome_options.add_argument('--no-sandbox')  # Dodaj, jeśli potrzebne
        chrome_options.add_argument('--disable-dev-shm-usage')  # Dodaj, jeśli potrzebne

        # Inicjalizacja WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        driver.get(url)

        try:
            # Oczekiwanie na załadowanie elementów recenzji
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "review-text"))
            )

            # Znajdź wszystkie elementy zawierające recenzje
            reviews_elements = driver.find_elements(By.CLASS_NAME, "review-text")

            # Pobierz tekst recenzji
            reviews = [review.text for review in reviews_elements]

            if reviews:
                st.write(f"Znaleziono {len(reviews)} recenzji:")
                for i, review in enumerate(reviews, start=1):
                    st.write(f"**Recenzja {i}:** {review}")
            else:
                st.write("Nie znaleziono recenzji na stronie.")

        except Exception as e:
            st.error(f"Wystąpił błąd: {str(e)}")

        finally:
            # Zakończ działanie przeglądarki
            driver.quit()
