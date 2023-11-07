from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType
from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus
import streamlit as st

st.header("Natural Language to SQL WebApp")

os.environ['OPENAI_API_KEY'] = 'Your API Key goes here'


#database connection details
DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'DESKTOP-0ASMS67\SQLEXPRESS'
DATABASE_NAME = 'AdventureWorks2022'

conn = f'DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};trusted_connection=yes'


quoted = quote_plus(conn)  
target_connection = 'mssql+pyodbc:///?odbc_connect={}'.format(quoted) 
engine = create_engine(target_connection)   



database = SQLDatabase(engine)    


#connecting with llm
llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)
toolkit = SQLDatabaseToolkit(db=database, llm=llm) 

agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit, 
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
)


#   creating prompt
prompt=st.text_input('Enter the question')


if st.button('Run'):
    final=agent_executor.run(prompt) 
    st.text(final) 




st.sidebar.write("Natural Language to SQL WebApp")
st.sidebar.markdown("[Streamlit](https://streamlit.io/)")
st.sidebar.markdown("[LangChain](https://python.langchain.com/)")
st.sidebar.markdown("Made by Abdul Ahad")
st.sidebar.markdown("LinkedIn:https://www.linkedin.com/in/abdul-ahad-24a342230/")