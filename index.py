from fastapi import FastAPI
from langchain_tavily import TavilySearch
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain.messages import SystemMessage,HumanMessage
from langchain.agents import create_agent
from dotenv import load_dotenv
app=FastAPI()
load_dotenv()


api_key_gem = os.getenv("api_key_gemini")

tavily_key=os.getenv("tavily_api_key")

class register(BaseModel):
    question:str


# v=[]

@app.get("/")
def hello():
    return "hello world"


@app.get("/abc")
def helloo():
    return {
        "hello":"hi"
    }
    
@app.post("/data")
def dataa(regsiter:register):
    model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=api_key_gem,
    )
    tavily_search=TavilySearch(
    tavily_api_key=tavily_key,
    max_results=3,
    topic="general",
    )
    search_agent=create_agent(
     model=model,
     tools=[tavily_search],
    # verbose=True,
     system_prompt=SystemMessage(
        """
        you are a search assistant
        for any question related to  current events or events after jan 2025,
        you must use the search tool and answer
        dont rely on internal knowledge


        """)

      )
    res=search_agent.invoke({
    "messages":[HumanMessage(
        regsiter.question
    )]
      })

    return {"message":res["messages"][-1].content[0]["text"]}


# @app.get("/data")
# def data_get():
#     return v

