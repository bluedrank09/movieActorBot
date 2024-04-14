import httpx # to do the actual calls to the webpages
import os
from dotenv import load_dotenv # to make environment variables program variables

def get_links(log, website, query_string):
    try:
        load_dotenv()
        GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
        GOOGLE_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')

        #getting response json - same parameters as postman. this will return a response object, wihch we turn into a json using response.json()
        params = {'q' : f"{query_string} {website}", 'key' : GOOGLE_API_KEY, 'cx' : GOOGLE_SEARCH_ENGINE_ID, 'num' : 1}
        response = httpx.get('https://www.googleapis.com/customsearch/v1', params = params)
        link = response.json()["items"][0]["link"]
        return(link)
        
    except Exception as error:
        log.error(error)
        raise(error)




