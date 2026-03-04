import streamlit as st
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ---------------- CONFIG ----------------
MAIN_DOMAIN = "vegatron.com.sg"

KEYWORDS = [
    "diesel supplier singapore",
    "bunker oil supplier",
    "bunker fuel supplier",
    "bunker supplier singapore",
    "Diesel Fuel",
    "diesel fuel delivery",
    "diesel delivery singapore",
    "diesel top up singapore",
    "diesel fuel supplier",
    "diesel supply singapore",
    "Emergency Diesel",
    "emergency diesel",
    "24/7 diesel",
    "Homepage",
    "refueling services",
    "diesel refueling services",
    "fuel management system",
    "diesel tanks",
    "lubricant oil supplier singapore",
    "oil and gas trading companies in singapore",
    "marine gas oil",
    "adblue singapore",
    "10ppm"
]

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Vegatron Rank Checker", layout="wide")
st.title("🚀 Vegatron Google Rank Checker")

def check_rankings():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    results = []

    for keyword in KEYWORDS:
        driver.get(f"https://www.google.com/search?q={keyword}")
        time.sleep(5)

        links = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")

        rank = "Not Found"
        matched_url = "-"

        position = 1
        for link in links:
            href = link.get_attribute("href")

            if MAIN_DOMAIN in href:
                rank = position
                matched_url = href
                break

            position += 1

        results.append({
            "Keyword": keyword,
            "Rank": rank,
            "Matched URL": matched_url
        })

    driver.quit()

    return pd.DataFrame(results)

# ---------------- START BUTTON ----------------
if st.button("Start"):
    with st.spinner("Checking rankings on Google..."):
        df = check_rankings()

    st.success("Ranking check completed!")
    st.dataframe(df, use_container_width=True)
