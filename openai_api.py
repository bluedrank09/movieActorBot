# importing libraries
import os 
from dotenv import load_dotenv # to make environment variables program variables
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI # to make the call to openai

def check_movie_actor(log, name):
    try:
        load_dotenv()
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

        prompt = PromptTemplate.from_template("""Question: is {name} a movie or an actor? answer with 'y' if it is a movie, 'n' if it is an actor, 'x' if it is neither""") # creating question for openai
        llm = OpenAI(openai_api_key=OPENAI_API_KEY) # getting the api key to talk to OpenAI
        llm_chain = LLMChain(prompt=prompt, llm=llm) # asking OpenAI the question
        log.info(f"{llm_chain.invoke(name)}---------!!!")
        llm_response = llm_chain.invoke(name) # getting response from OpenAI
        filter_llm_response = filter(str.isalpha, llm_response['text'])
        type_flag = "".join(filter_llm_response)
        log.info(f" THE FLAG IS {type_flag}, text is {llm_response}")
        return(type_flag)
    except Exception as error:
        log.error(error)
        raise error