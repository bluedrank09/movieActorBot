import streamlit as st

moviesColumn, emptyThree, actorColumn = st.columns(3)
with moviesColumn:
    movieOptions = st.radio("***Movies***", ["General Info", "Cast and Crew", "Reviews"], captions = ["The movie synposis and ideas", "Who acted and helped in the film", "Opinions and ratings of the movie"])
with emptyThree:    
    st.write("")
with actorColumn:
    actorOptions = st.radio("***Actors***", ["Biography", "Box Office", "Filmography"], captions = ["Basic information about them", "How well they've done in the box office", "Movies and TV shows they have acted in"])
    st.write("")