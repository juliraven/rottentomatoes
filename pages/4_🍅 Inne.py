from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Funkcja do pobierania recenzji przy użyciu Selenium
def scrape_reviews_selenium(url):
    # Konfiguracja opcji przeglądarki w trybie headless
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument("--disable-gpu")

    # Automatyczne pobranie najnowszej wersji Edge WebDriver
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)
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

        # Sprawdź, czy recenzje zostały znalezione
        if not reviews:
            st.write("Nie znaleziono recenzji na stronie.")
        return reviews

    except Exception as e:
        st.write(f"Wystąpił błąd: {str(e)}")
        return []

    finally:
        driver.quit()

# Interfejs użytkownika w Streamlit
url = st.text_input("https://www.rottentomatoes.com/m/terrifier_3/reviews")

if st.button('Fetch and Analyze Reviews'):
    with st.spinner('Fetching reviews...'):
        reviews = scrape_reviews_selenium(url)
        if reviews:
            st.write(f"Found {len(reviews)} reviews")
            for i, review in enumerate(reviews, start=1):
                st.write(f"**Review {i}:** {review}")
                st.write("---")
        else:
            st.write("No reviews found on this page.")

