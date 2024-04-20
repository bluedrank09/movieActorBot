import streamlit as st

moviesColumn, emptyThree, actorColumn = st.columns(3)
with moviesColumn:
    movie_options = st.radio("***Movies***", ["General Info", "Cast and Crew", "Reviews"], captions = ["The synopsis and fun facts of the movie", "Actors and crew on the movie", "Reviews and ratings of the film"])
with emptyThree:    
    st.write("")
with actorColumn:
    actor_options = st.radio("***Actors***", ["Biography", "Awards", "Filmography"], captions = ["About them and their life", "Awards and accomplishments they've won", "Movies and TV shows they're in"])

st.text_input('Name of actor or movie', placeholder="Type here...")