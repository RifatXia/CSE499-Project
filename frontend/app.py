import streamlit as st
from streamlit import components

# Set the page title

with open("../frontend/index.html", "r") as file:
    html_content = file.read()
    st.write(html_content, unsafe_allow_html=True)
