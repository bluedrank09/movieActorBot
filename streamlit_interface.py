# importing libraries
import streamlit as st # streamlit is the package that handles the actual GUI
import logging # for logger to replace print statements 
from openai_api import check_movie_actor # importing function to check movie or actor from other file
from google_api import get_links
import time
import math

def main():
    try:
        logging.basicConfig(level = logging.INFO, format = "[{asctime}] - {funcName} - {lineno} - {message}", style = '{')
        log = logging.getLogger("movie_actors_links")

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
        print(f"-------------!!!-----{st.session_state.clicked} st session state")

        def clicked(button):
            st.session_state.clicked[button] = True
            print(f"-------------!!!-----{st.session_state.clicked} st session state AFTER CLICKING BUTTON")

        name = st.text_input('Name of actor or movie', placeholder="Type here...")

        with st.container(): # to align submit button
            empty_one, submitButton, empty_two = st.columns(3)
            with empty_one:
                st.write("")
            with submitButton:
                st.button('Submit', on_click=clicked, args=[1])
            with empty_two:
                st.write("")
                    
        if st.session_state.clicked[1]:
            if name == "": # checking if there is no name inputted
                st.error('Please input a name', icon="🚨")
                log.info("No input from user. Please input a name")
            else: # checking if the user inputted the name of an actor or a movie
                with st.spinner("Loading..."):
                    # call to openai_api.py file / getting whether the name is actor or movie
                    # y means movie, n means actor
                    type_flag = check_movie_actor(log, name)
                    time.sleep(1)

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

                empty_four, ask_button_column, empty_five = st.columns(3)
                with empty_four:
                    st.write("")
                with ask_button_column:
                    st.button('Ask', on_click=clicked, args=[2]) # ask button for the name AND radio option        
                with empty_five:
                    st.write("")

            if st.session_state.clicked[2]:
                st.session_state.clicked = {1:False,2:True}
                if type_flag == 'y': # options if the user inputted 
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

                progress_text = "Fetching links to websites..."
                websites_progress_bar = st.progress(0, text=progress_text)
                
                websites_list = ['wikipedia', 'imdb', 'rotten tomatoes'] # list of websites
                for index, website in enumerate(websites_list):
                    link = get_links(log, website, query_string)
                    match website:
                        case 'wikipedia':
                            link_wikipedia = link
                        case 'imdb':
                            link_imdb = link
                        case 'rotten tomatoes':
                            link_rotten_tomatoes = link
                        
                    websites_progress_bar.progress(((math.trunc(100/3))*(index + 1)), text=f"{progress_text}fetching link from {website}...") # progress bar
                    time.sleep(0.75) # sleep so user can see the progress bar moving
                
                websites_progress_bar.empty() # emptying progress bar and making it disappear once websites have been fetched

                with st.expander("Wikipedia"): # expander for wikipedia
                    st.page_link(link_wikipedia, label="Wikipedia", icon="🌎") # st widget that displays link   

                with st.expander("IMDB"): # expander for imdb
                    st.page_link(link_imdb, label="IMDB", icon="🌎") # st widget that displays link 

                with st.expander("Rotten Tomatoes"): # expander for rotten tomatoes
                    st.page_link(link_rotten_tomatoes, label="Rotten Tomatoes", icon="🌎") # st widget that displays link

                st.session_state.clicked = {1:False,2:False} # so that when user runs program again, they can strat from the real beginning
                print(f"-------------!!!-----{st.session_state.clicked} after all buttons cliced program finished")
                # response.json is an object. It is made of dictionaries and lists. response.json() is a list, item is the index
    except Exception as error:
        raise error
    
    finally:
        log.info(f":D")

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)   
