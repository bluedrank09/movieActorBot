# importing libraries - streamlit and httpx are third paty - pip installed as they don't exist in the environment at first
import streamlit as st # streamlit is the package that handles the actual GUI
import pandas as pd # to create a dataframe
from dotenv import load_dotenv # to make environment variables program variables
import os
import httpx # to do the actual calls to the webpages
import streamlit.components.v1 as components # to render html page
import math # for the progress bar - to get the correcet percentage of websites fetched
import time # for the progress bar 
import logging as log
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

st.set_page_config(page_title="Movies and Actors 'Google'")

# hiding the "deploy", "rerun", "rerun always" options from the top right of the screen
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# streamlit widgetss
st.title("Movies and Actors 'Google'")

name = st.text_input('Name of actor or movie', placeholder="Type here...")

moviesColumn, emptyThree, actorColumn = st.columns(3)
with moviesColumn:
    st.write("Movie options:")
    cast_list = st.checkbox('Cast List')
    box_office = st.checkbox('Box Office')
    fun_trivia = st.checkbox('Fun Trivia')
with emptyThree:    
    st.write("")
with actorColumn:
    st.write("Actor options:")
    list_of_movies = st.checkbox('List of movies')
    statistics = st.checkbox('Statistics')
    fun_facts = st.checkbox('Fun Facts')

with st.container():
    emptyOne, submitButton, emptyTwo = st.columns(3)
    with emptyOne:
        st.write("")
    with submitButton:
        submit = st.button('Submit')
    with emptyTwo:
        st.write("")

#numberOfCheckboxes = 0

if submit:
    if name == "": # checking if there is no name inputted
        st.error('Please input a name', icon="🚨")
        #print("No input from user. Please input a name")
    else:
        if cast_list:
            query_string = name + " cast list"
            #numberOfCheckboxes = 1
            #print(numberOfCheckboxes)
        elif box_office:
            query_string = name + " box office"
            #numberOfCheckboxes = 1
            #print(numberOfCheckboxes)
        elif fun_trivia:
            query_string = name + " fun trivia"
            #numberOfCheckboxes = 1
            #print(numberOfCheckboxes)
        elif list_of_movies:
            query_string = name + " list of movies"
            #numberOfCheckboxes = 1
            #print(numberOfCheckboxes)
        elif statistics:
            query_string = name + " statistics"
            #numberOfCheckboxes = 1
            #print(numberOfCheckboxes)
        elif fun_facts:
            query_string = name + " fun facts"
            #numberOfCheckboxes = 1
            #print(f"{numberOfCheckboxes} -----------------!")
        else:
            noCheckboxes = st.text_area = "Please select a text box"
            st.write(noCheckboxes)

        #print(numberOfCheckboxes)

        # if numberOfCheckboxes > 1:
        #     tooManyCheckboxes = st.text_area = "Please select a text box"
        #     st.write(tooManyCheckboxes)

        #print(query_string)


    #try: # try except finally for error handling
        # making the varibales in .env os variables
        load_dotenv()
        # making then program variables
        GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
        GOOGLE_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

        prompt = PromptTemplate.from_template("""Question: is {name} a movie or an actor? reply y for movie, n for actor""") # creating question for openai
        llm = OpenAI(openai_api_key=OPENAI_API_KEY)
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        print(llm_chain.invoke(name))

        link_wikipedia = ""
        link_imdb = ""
        link_rotten_tomatoes = ""
        
        progress_text = "Fetching links to websites..."
        websites_progress_bar = st.progress(0, text=progress_text)

        websites_list = ['wikipedia', 'imdb', 'rotten tomatoes']
        for index, website in enumerate(websites_list):
            #print(website)
            #getting response json - same parameters as postman. this will return a response object, wihch we turn into a json using response.json()
            params = {'q' : f"{query_string} {website}", 'key' : GOOGLE_API_KEY, 'cx' : GOOGLE_SEARCH_ENGINE_ID, 'num' : 1}
            response = httpx.get('https://www.googleapis.com/customsearch/v1', params = params)
            websites_progress_bar.progress(((math.trunc(100/3))*(index + 1)), text=f"{progress_text}fetching website {index + 1}...") # progress bar
            time.sleep(0.75)

            # if response.status_code == 200 : # 200OK means that the call to the url worked. response.status_code is an iteger value. 403 means forbidden
                    # print(f"Web call to {website} suceeded with {response.status_code}")

            match index:
                case 0:
                    link_wikipedia = response.json()["items"][0]["link"]
                    # print(f"{link_wikipedia=}")
                case 1:
                    link_imdb = response.json()["items"][0]["link"]
                    # print(f"{link_imdb=}")
                case 2:
                    link_rotten_tomatoes = response.json()["items"][0]["link"]
                    # print(f"{link_rotten_tomatoes=}")

        websites_progress_bar.empty()

        with st.expander("Wikipedia"):
            st.page_link(link_wikipedia, label="Wikipedia", icon="🌎")       

        with st.expander("IMDB"):
            st.page_link(link_imdb, label="IMDB", icon="🌎")   

        with st.expander("Rotten Tomatoes"):
        #components.iframe("https://www.example.org", height=400, scrolling=True)
            st.page_link(link_rotten_tomatoes, label="Rotten Tomatoes", icon="🌎")   
        

    # response.json is an object. It is made of dictionaries and lists. response.json() is a list, item is the index

