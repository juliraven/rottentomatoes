import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# The Service class is used to start an instance of the Chrome WebDriver
# The no-argument constructor means it will look for the WebDriver executable in the system's PATH
service = Service()

# WebDriver.ChromeOptions() is used to set the preferences for the Chrome browser
options = webdriver.ChromeOptions()

# Here, we start an instance of the Chrome WebDriver with the defined options and service
driver = webdriver.Chrome(service=service, options=options)

# Your code for interacting with web pages goes here

# In the end, always close or quit the driver to ensure all system resources are freed up
driver.quit()


