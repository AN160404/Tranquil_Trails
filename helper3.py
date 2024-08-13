import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv('hello.env')
api_key = os.getenv("api_key")
os.environ["api_key"]="api_key"

llm=GoogleGenerativeAI(google_api_key=api_key,model='models/text-bison-001', temperature=0.9)

# llm=google_palm(google_api_key=api_key,temperature=0.6)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
e = embeddings.embed_query("Goa")
len(e)
instructor_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", task_type="retrieval_query"
) 

vectordb_file_path = "faiss_index"
def create_vector_db():
 
 loader = CSVLoader(file_path="project.csv", source_column="States + UTs")
 data = loader.load()
 
 
 

 vectordb = FAISS.from_documents(documents=data,embedding=instructor_embeddings)
 vectordb.save_local(vectordb_file_path)
#  retriever = vectordb.as_retriever(score_threshold = 0.7)
#  rdocs = retriever.get_relevant_documents("" meditation")
#  rdocs
def get_qa_chain():
   vectordb = FAISS.load_local(vectordb_file_path, instructor_embeddings, allow_dangerous_deserialization=True)
   retriever = vectordb.as_retriever(score_threshold = 0.7)
   prompt_template = """Given the following context and a question, generate an answer based on this context only.
   In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
   If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

    CONTEXT: {context}

  QUESTION: {question}
  Please provide a detailed and comprehensive answer that includes multiple aspects and detailed explanations where possible.
  """
   PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"])
   chain_type_kwargs = {"prompt": PROMPT}
   chain = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=retriever, input_key="query",return_source_documents=True, chain_type_kwargs=chain_type_kwargs)

   return chain

   
   




# prompt_template = """Given the following context and a question, generate an answer based on this context only.
# In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
# If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

# CONTEXT: {context}

# QUESTION: {question}"""


# PROMPT = PromptTemplate(
#     template=prompt_template, input_variables=["context", "question"]
# )
# chain_type_kwargs = {"prompt": PROMPT}
# chain = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=retriever, input_key="query",return_source_documents=True, chain_type_kwargs=chain_type_kwargs)
# chain("what is yoga")
# return chain

if __name__ == "__main__":
    create_vector_db()
    chain = get_qa_chain()