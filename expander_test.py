import streamlit as st

link_wikipedia = "https://en.wikipedia.org/wiki/Brooklyn_Nine-Nine"
link_imdb = "https://en.wikipedia.org/wiki/Brooklyn_Nine-Nine"
link_rotten_tomatoes =  "https://en.wikipedia.org/wiki/Brooklyn_Nine-Nine"

with st.expander("Wikipedia"): # expander for wikipedia
    st.page_link(link_wikipedia, label="Wikipedia", icon="🌎") # st widget that displays link   

with st.expander("IMDB"): # expander for imdb
    st.page_link(link_imdb, label="IMDB", icon="🌎") # st widget that displays link 

with st.expander("Rotten Tomatoes"): # expander for rotten tomatoes
    st.page_link(link_rotten_tomatoes, label="Rotten Tomatoes", icon="🌎")