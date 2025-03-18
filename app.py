import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8765/v1/retrieve"

st.title("Digital Neocortex Dashboard")

st.header("Memory Recall")
query_text = st.text_input("Enter your memory recall query:", "Recall the most recent sensor interactions at home")
k = st.number_input("Number of results", min_value=1, max_value=10, value=3, step=1)

if st.button("Retrieve Memory"):
    payload = {"query": query_text, "k": k}
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.write("No matching documents found.")
    except Exception as e:
        st.error(f"Error: {e}")

st.header("Prediction Engine (Coming Soon)")
st.write("This section will eventually display upcoming alerts and predictions based on your interactions.")

