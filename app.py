import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('hello.env')

# Retrieve the API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")

# Ensure the API key is available
if not api_key:
    st.error("Google API key is missing. Please check your .env file.")
else:
    # Initialize GoogleGenerativeAI
    llm = GoogleGenerativeAI(google_api_key=api_key, model='models/text-bison-001', temperature=0.9)

    # Initialize embeddings
    instructor_embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", task_type="retrieval_query"
    ) 

    vectordb_file_path = "faiss_index"

    def create_vector_db():
        loader = CSVLoader(file_path="project.csv", source_column="States + UTs")
        data = loader.load()
        vectordb = FAISS.from_documents(documents=data, embedding=instructor_embeddings)
        vectordb.save_local(vectordb_file_path)
        st.success("Vector database created and saved.")

    def get_qa_chain():
        vectordb = FAISS.load_local(vectordb_file_path, instructor_embeddings, allow_dangerous_deserialization=True)
        retriever = vectordb.as_retriever(score_threshold=0.7)
        prompt_template = """Given the following context and a question, generate an answer based on this context only.
        In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
        If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

        CONTEXT: {context}

        QUESTION: {question}
        Please provide a detailed and comprehensive answer that includes multiple aspects and detailed explanations where possible.
        """
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"prompt": PROMPT}
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            input_key="query",
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs
        )
        return chain

    # Streamlit app components
    st.title("Document Search and Q&A")

    if st.button("Create Vector Database"):
        create_vector_db()

    question = st.text_input("Enter your question:")
    if st.button("Get Answer") and question:
        chain = get_qa_chain()
        answer = chain(question)
        st.write(answer)
