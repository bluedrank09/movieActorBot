# importing libraries - streamlit and httpx are third paty - pip installed as they don't exist in the environment at first
import streamlit as st # streamlit is the package that handles the actual GUI
import pandas as pd # to create a dataframe
from dotenv import load_dotenv 
import os
import httpx # to do the actual calls to the webpages
import streamlit.components.v1 as components # to render html page

# streamlit widgetss
st.title('lol')
name = st.text_input('Name of actor or movie :')
cast_list = st.checkbox('Cast List')
box_office = st.checkbox('Box Office')
fun_trivia = st.checkbox('Fun Trivia')
list_of_movies = st.checkbox('List of movies')
statistics = st.checkbox('Statistics')
fun_facts = st.checkbox('Fun Facts')
submit = st.button('Submit')

if submit:
    if cast_list:
        query_string = name + " cast list"
    if box_office:
        query_string = name + " box office"
    if fun_trivia:
        query_string = name + " fun trivia"
    if list_of_movies:
        query_string = name + " list of movies"
    if statistics:
        query_string = name + " statistics"
    if fun_facts:
        query_string = name + " fun facts"

    print(query_string)


    #try: # try except finally for error handling
        # making the varibales in .env os variables
    load_dotenv()
    # making then program variables
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    GOOGLE_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')

    link_wikipedia = ""
    link_imdb = ""
    link_rotten_tomatoes = ""

    websites_list = ['wikipedia', 'imdb', 'rotten tomatoes']
    for index, website in enumerate(websites_list):
        print(website)
        #getting response json - same parameters as postman. this will return a response object, wihch we turn into a json using response.json()
        params = {'q' : f"{query_string} {website}", 'key' : GOOGLE_API_KEY, 'cx' : GOOGLE_SEARCH_ENGINE_ID, 'num' : 1}
        response = httpx.get('https://www.googleapis.com/customsearch/v1', params = params)

        #print(response.json()["items"][0]["link"])
        
        if response.status_code == 200 : # 200OK means that the call to the url worked. response.status_code is an iteger value. 403 means forbidden
                print(f"Web call to {website} suceeded with {response.status_code}")

        match index:
            case 0:
                link_wikipedia = response.json()["items"][0]["link"]
                print(f"{link_wikipedia=}")
            case 1:
                link_imdb = response.json()["items"][0]["link"]
                print(f"{link_imdb=}")
            case 2:
                link_rotten_tomatoes = response.json()["items"][0]["link"]
                print(f"{link_rotten_tomatoes=}")

    with st.expander("Wikipedia"):
        st.page_link(link_wikipedia, label="Wikipedia", icon="🌎")       

    with st.expander("IMDB"):
        st.page_link(link_imdb, label="IMDB", icon="🌎")   

    with st.expander("Rotten Tomatoes"):
    #components.iframe("https://www.example.org", height=400, scrolling=True)
        st.page_link(link_rotten_tomatoes, label="Rotten Tomatoes", icon="🌎")   
    

    # response.json is an object. It is made of dictionaries and lists. response.json() is a list, item is the index
    # for index, item in enumerate(response.json()["items"]): # iteration --- item in place of i. to iterate through all three urls in the items
    #     json_url = item["link"] 
        
        #print(f"URL {item} - {json_url}")
        #response = httpx.get(json_url) # reponse is NOT a python keyword. it could be called anything

        
            #webpage_contents = response.text
           # print(f"{index=}")

            

            #print(webpage_contents) # priting out the webpage contexts. originally it is a json. we convert it to text. we then print out the url contents, as webpages are all in text
        #else: # error handling
        #    print(f"Web call to {json_url} failed with {response.status_code}")

    
            
    # except Exception as error: # error handling
    #     raise error

# # if __name__ == "__main__":
#     try:
#         #main() # main function is seperate to keep code clean
#         pass
#     except Exception as error: # error handling
#         print(error)    
#         raise error
#     finally:
#         #print(f":D")
#         print(f":D")

        # MUST DO :
        # 1. containers for streamlit to alogn everyting on the webpage
        # 2. figure out carousel for the three webpages
        # 3. how to render webpages with streamlit
        # 4. error handling and displaying error messages
    
        
