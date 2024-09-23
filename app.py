import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from hello import api_key  # Assuming this is where the API key is stored
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_core.runnables import RunnablePassthrough

# Set the API key in the environment
os.environ["GOOGLE_API_KEY"] = api_key

# Initialize the Google Generative AI model for question-answering
llm = GoogleGenerativeAI(google_api_key=api_key, model='gemini-1.5-flash', temperature=0.9)

# Initialize embeddings model for retrieval
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


# Create another embedding for query retrieval
instructor_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", task_type="retrieval_query"
)

# Path to save/load the FAISS vector database
vectordb_file_path = "faiss_index"

# Function to create the vector database from a CSV file
def create_vector_db():
    # Load the CSV file, assuming there's a column called 'States + UTs' containing the relevant data
    loader = CSVLoader(file_path="project.csv", source_column="States + UTs")
    data = loader.load()

    # Create the vector store using FAISS and store locally
    vectordb = FAISS.from_documents(documents=data, embedding=instructor_embeddings)
    vectordb.save_local(vectordb_file_path)

# Function to set up the QA chain
def get_qa_chain():
    # Load the vector database
    vectordb = FAISS.load_local(vectordb_file_path, instructor_embeddings, allow_dangerous_deserialization=True)

    # Set up the retriever with a score threshold to filter relevant documents and return top 5 chunks
    retriever = vectordb.as_retriever(score_threshold=0.7, top_k=5)

    # Define the prompt template
    prompt_template = """
   You are an expert assistant in tourism and travel planning. Based on the following context retrieved from a document, generate a complete and detailed answer to the user's question.

   Make sure the response is well-structured, includes practical recommendations, and explains the content clearly. Avoid using phrases such as "the document says" and aim to provide a natural response.

   CONTEXT: {context}

  QUESTION: {question}

   Answer as thoroughly as possible, combining information from the context and offering additional suggestions if relevant. If the answer is not found in the context, say "I don't know" and avoid creating false information.
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # Create a RAG chain using the retriever, prompt, and LLM
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    return chain
