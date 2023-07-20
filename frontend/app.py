import streamlit as st
from streamlit import components

# Set the page title

with open("CSE499-Project\\frontend\index.html", "r") as file:
    html_content = file.read()
    st.write(html_content, height=800, scrolling=True)







