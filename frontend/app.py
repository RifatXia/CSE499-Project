import streamlit as st
from streamlit import components

# Set the page title

with open("index.html", "r") as file:
    html_content = file.read()
st.components.v1.html(html_content, height=800, scrolling=True)

