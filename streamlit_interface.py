# importing libraries
import streamlit as st # streamlit is the package that handles the actual GUI
import logging # for logger to replace print statements 
from openai_api import check_movie_actor # importing function to check movie or actor from other file
from google_api import get_links
import time
import math # for the progess bar

def main():
    try:
        # setting up logging system for debugging 
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

        def clicked(button): # setting what clicked means - the program will know to execture 'True' code when button is clicked
            st.session_state.clicked[button] = True

        name = st.text_input('Name of actor or movie', placeholder="Type here...") # inut area for user to type name
        st.write("*Note : To ask another question, please reload the tab*") # note for if they want to ask multiple questions

        with st.container(): # to align submit button
            empty_one, submit_button, empty_two = st.columns(3)
            with empty_one:
                st.write("")
            with submit_button:
                st.button('Submit', on_click=clicked, args=[1])
            with empty_two:
                st.write("")
                    
        if st.session_state.clicked[1]: # if submit button clicked
            if name == "": # checking if there is no name inputted
                st.error('Please input a name', icon="🚨")
                log.info("No input from user. Please input a name")
            else: # checking if the user inputted the name of an actor or a movie
                with st.spinner("Loading..."): # creating spinner to display while program goes to openai
                    # call to openai_api.py file / getting whether the name is actor or movie
                    # y means movie, n means actor
                    type_flag = check_movie_actor(log, name) # using method from openai_api.py
                    time.sleep(1)

                # setting radio options
                movies_column, empty_three, actor_column = st.columns(3) # creating columns to align 
                if type_flag == 'y': # setting radio options for if the name is a movie name
                    with movies_column:
                        movie_options = st.radio("***Movies***", ["General Info", "Cast and Crew", "Reviews"], captions = ["The synopsis and fun facts of the movie", "Actors and crew on the movie", "Reviews and ratings of the film"])
                    with empty_three:    
                        st.write("")
                elif type_flag == 'n': # setting radio options for if the name is an actor name
                    with actor_column:
                        actor_options = st.radio("***Actors***", ["Biography", "Awards", "Filmography"], captions = ["About them and their life", "Awards and accomplishments they've won", "Movies and TV shows they're in"])
                        st.write("")
                elif type_flag == 'x': # raising an error is the name user inputted is neither a movie or actor - invalid
                    st.error("Please input the name of a movie or actor", icon="🚨")

                empty_four, ask_button_column, empty_five = st.columns(3) # column to align ask button for name and radio option chosen by user
                with empty_four:
                    st.write("")
                with ask_button_column: 
                    if type_flag == 'y': 
                        ask = st.button('Ask', on_click=clicked, args=[2]) # allowing button to be clicked if name is valid - movie
                    elif type_flag == 'n': 
                        ask = st.button('Ask', on_click=clicked, args=[2]) # allowing button to be clicked if name is valid - actor
                    elif type_flag == 'x':
                        ask = st.button('Ask', on_click=clicked, args=[2], disabled=True) # setting button to be disabed if the name was invalid
                with empty_five:
                    st.write("")

            if st.session_state.clicked[2]: # if ask button clicked
                if type_flag == 'y': # creating query string if/with a movie name and the radio the user chose 
                    if movie_options == 'General Info':
                        query_string = name + " general info"
                    elif movie_options == 'Cast and Crew':
                        query_string = name + " cast and crew"
                    elif movie_options == 'Reviews':
                        query_string = name + " reviews"
                elif type_flag == 'n': # creating query string if/with a actor name and the radio the user chose 
                    if actor_options == 'Biography':
                        query_string = name + " biography"
                    elif actor_options == 'Awards':
                        query_string = name + " awards"
                    elif actor_options == 'Filmography':
                        query_string = name + " filmography"

                #progress bar text while websites are being fetched
                progress_text = "Fetching links to websites..."
                websites_progress_bar = st.progress(0, text=progress_text)
                
                websites_list = ['wikipedia', 'imdb', 'rotten tomatoes'] # list of websites
                for index, website in enumerate(websites_list):
                    link = get_links(log, website, query_string) # using function from google_api.py
                    match website: 
                        case 'wikipedia': 
                            link_wikipedia = link # stroing wikipedia link 
                        case 'imdb':
                            link_imdb = link # storing imdb link
                        case 'rotten tomatoes':
                            link_rotten_tomatoes = link # storing rotten tomatoes link

                    # ((math.trunc(100/3))*(index + 1)) shows even three step progress on the progress bar  
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
                
    except Exception as error: # raising potential errors
        raise error
    
    finally:
        log.info(f":D") # logging :D lol

if __name__ == "__main__":
    try:
        main() # calling main function
    except Exception as error:
        print(error) # raising potential errors
