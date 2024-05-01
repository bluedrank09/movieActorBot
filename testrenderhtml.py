import streamlit.components.v1 as components
import streamlit as st
import webbrowser as wb

with st.expander("Expand here:"):
    components.html("<html><body><h1>In God we trust</h1></body></html>")

with st.expander("Expand here 2:"):
    st.write("All other must pay in cash")

with st.expander("Expand here test:"):
    components.iframe("https://www.example.org", height=400, scrolling=True)

wb.open_new('https://www.imdb.com/title/tt2906216/')

# st.header("test html import")

# HtmlFile = open("test.html", 'r', encoding='utf-8')
# source_code = HtmlFile.read() 
# print(source_code)
# components.html(source_code
