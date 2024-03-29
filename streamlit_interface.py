# libraries
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import httpx

st.title('lol')
name = st.text_input('Name of actor or movie :')
st.checkbox('Cast List')
st.checkbox('Box Office')
st.checkbox('Fun Trivia')
st.checkbox('List of movies')
st.checkbox('Statistics')
st.checkbox('Fun Facts')
st.button('Submit')

def main():
    try:
        # making the varibales in .env os variables
        load_dotenv()
        # making then program variables
        GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
        GOOGLE_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
        # printing
        print(f"{GOOGLE_API_KEY=}")
        print(f"{GOOGLE_SEARCH_ENGINE_ID=}")

        #getting response json - same parameters as postman
        params = {'q' : 'benedict cumberbatch', 'key' : GOOGLE_API_KEY, 'cx' : GOOGLE_SEARCH_ENGINE_ID, 'num' : 3}
        response = httpx.get('https://www.googleapis.com/customsearch/v1', params = params)
        print(response.json())

    except Exception as error:
        raise error

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)    
        raise error
    finally:
        print(f":D")
    
        
