import streamlit as st

st.set_page_config(page_title="Analiza Sentymentu")

# Tworzenie zakładek
tab1, tab2, tab3 = st.tabs(["Home", "Analysis", "Settings"])

# Treść zakładki "Home"
with tab1:
    st.header("Home")
    st.write("This is the home page.")

# Treść zakładki "Analysis"
with tab2:
    st.header("Analysis")
    st.write("This is the analysis page.")

# Treść zakładki "Settings"
with tab3:
    st.header("Settings")
    st.write("This is the settings page.")

st.markdown(
    """
    <style>
    .emoji-top {
        margin-top: -20px; /* Zmniejszenie marginesu górnego */
    }
    </style>
    
    <div style="text-align: center;">
        <h1 class="emoji-top">🍅 🍅 🍅</h1> 
        <h2>Analiza sentymentu recenzji filmowych na podstawie recenzji użytkowników strony</h2>
    </div>
    """, 
    unsafe_allow_html=True
)

st.image('tomato.png', use_column_width=True)

