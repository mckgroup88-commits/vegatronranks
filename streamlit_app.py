import streamlit as st
import pandas as pd
import requests

# ---------------- CONFIG ----------------
API_KEY = "YOUR_GOOGLE_API_KEY"  # Replace with your Google Custom Search API key
CX = "YOUR_SEARCH_ENGINE_ID"     # Replace with your Custom Search Engine ID
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

def get_google_rank(keyword):
    """Query Google Custom Search API and return the rank and URL of the first matching MAIN_DOMAIN"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": keyword,
        "num": 10  # number of results per query
    }

    response = requests.get(url, params=params).json()
    results = response.get("items", [])

    rank = "Not Found"
    matched_url = "-"

    for i, item in enumerate(results, 1):
        link = item.get("link", "")
        if MAIN_DOMAIN in link:
            rank = i
            matched_url = link
            break

    return rank, matched_url

def check_all_keywords():
    """Loop through keywords and get rank info"""
    data = []
    for keyword in KEYWORDS:
        rank, url = get_google_rank(keyword)
        data.append({
            "Keyword": keyword,
            "Rank": rank,
            "Matched URL": url
        })
    return pd.DataFrame(data)

# ---------------- START BUTTON ----------------
if st.button("Start"):
    with st.spinner("Checking rankings on Google..."):
        df = check_all_keywords()

    st.success("Ranking check completed!")
    st.dataframe(df, use_container_width=True)
