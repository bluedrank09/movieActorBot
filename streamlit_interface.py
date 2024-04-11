# importing libraries
import streamlit as st # streamlit is the package that handles the actual GUI
from dotenv import load_dotenv # to make environment variables program variables
import os # to be ab
import httpx # to do the actual calls to the webpages
import math # for the progress bar - to get the correcet percentage of websites fetched
import time # for the progress bar 
import logging as log # for logger to replace print statements 
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI # to make the call to openai

st.set_page_config(page_title="Movies and Actors 'Google'") # name of tab

# hiding the "deploy", "rerun", "rerun always" options from the top right of the screen
hide_streamlit_style = """ 
    <style> 
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;} 
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.title("Movies and Actors 'Google'") # title of page

if 'clicked' not in st.session_state: # setting both buttons to False - not clicked
    st.session_state.clicked = {1:False,2:False}

def clicked(button):
    st.session_state.clicked[button] = True

name = st.text_input('Name of actor or movie', placeholder="Type here...")
with st.container(): # to align submit button
    emptyOne, submitButton, emptyTwo = st.columns(3)
    with emptyOne:
        st.write("")
    with submitButton:
        submit = st.button('Submit', on_click=clicked, args=[1])
    with emptyTwo:
        st.write("")
            
# making the varibales in .env os variables
load_dotenv() 
# making then program variables
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

#display_ask_flag = False

#print(f" display ask button flag is {display_ask_flag}")
if st.session_state.clicked[1]:
    if name == "": # checking if there is no name inputted
        st.error('Please input a name', icon="🚨")
        #print("No input from user. Please input a name")
    else: # checking if the user inputted the name of an actor or a movie
        prompt = PromptTemplate.from_template("""Question: is {name} a movie or an actor? answer with 'y' if it is a movie, 'n' if it is an actor, 'x' if it is neither""") # creating question for openai
        llm = OpenAI(openai_api_key=OPENAI_API_KEY) # getting the api key to talk to OpenAI
        llm_chain = LLMChain(prompt=prompt, llm=llm) # asking OpenAI the question
        # print(f"{llm_chain.invoke(name)}---------!!!")
        llm_response = llm_chain.invoke(name) # getting response from OpenAI
        type_flag = llm_response['text'][-1]
        print(f" THE FLAG IS {type_flag}, text is {llm_response}")

        moviesColumn, emptyThree, actorColumn = st.columns(3) # creating columns to align 
        if type_flag == 'y':
            with moviesColumn:
                movieOptions = st.radio("***Movies***", ["General Info", "Cast and Crew", "Reviews"], captions = ["a", "b", "c"])
            with emptyThree:    
                st.write("")
        elif type_flag == 'n':
            with actorColumn:
                actorOptions = st.radio("***Actors***", ["Biography", "Movies", "Filmography"], captions = ["d", "e", "f"])
                st.write("")
        empty_four, ask_button_column, emptyFive = st.columns(3)
        with empty_four:
            st.write("")
        with ask_button_column:
            ask_button = st.button('Ask', on_click=clicked, args=[2]) # ask button for the name AND radio option        
        with emptyFive:
            st.write("")

    if st.session_state.clicked[2]:
        #print(f"actors {actorOptions}")
        if type_flag == 'y':
            if movieOptions == 'General Info':
                query_string = name + " general info"
            elif movieOptions == 'Cast and Crew':
                query_string = name + " cast and crew"
            elif movieOptions == 'Reviews':
                query_string = name + " reviews"
        elif type_flag == 'n':
            if actorOptions == 'Biography':
                query_string = name + " biography"
            elif actorOptions == 'Movies':
                query_string = name + " movies"
            elif actorOptions == 'Filmography':
                query_string = name + " filmography"
        else:
            st.error('Please select an option', icon="🚨") # in case the user doesn't choose a radio option 

        # initialisng link vairables
        link_wikipedia = ""
        link_imdb = ""
        link_rotten_tomatoes = ""
        
        progress_text = "Fetching links to websites..."
        websites_progress_bar = st.progress(0, text=progress_text)

        websites_list = ['wikipedia', 'imdb', 'rotten tomatoes'] # list of websites
        for index, website in enumerate(websites_list):
            #print(website)
            #getting response json - same parameters as postman. this will return a response object, wihch we turn into a json using response.json()
            params = {'q' : f"{query_string} {website}", 'key' : GOOGLE_API_KEY, 'cx' : GOOGLE_SEARCH_ENGINE_ID, 'num' : 1}
            response = httpx.get('https://www.googleapis.com/customsearch/v1', params = params)
            websites_progress_bar.progress(((math.trunc(100/3))*(index + 1)), text=f"{progress_text}fetching website {index + 1}...") # progress bar
            time.sleep(0.75) # sleep so user can see the progress bar moving

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

        websites_progress_bar.empty() # emptying progress bar and making it disappear once websites have been fetched

        with st.expander("Wikipedia"): # expander for wikipedia
            st.page_link(link_wikipedia, label="Wikipedia", icon="🌎") # st widget that displays link   

        with st.expander("IMDB"): # expander for imdb
            st.page_link(link_imdb, label="IMDB", icon="🌎") # st widget that displays link 

        with st.expander("Rotten Tomatoes"): # expander for rotten tomatoes
            st.page_link(link_rotten_tomatoes, label="Rotten Tomatoes", icon="🌎") # st widget that displays link

    else:
        st.write("Button not pressed")    
    # response.json is an object. It is made of dictionaries and lists. response.json() is a list, item is the index

