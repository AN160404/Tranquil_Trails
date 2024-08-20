import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import nltk
from rouge_score import rouge_scorer

# Download necessary NLTK data
nltk.download('punkt')

# Load environment variables
load_dotenv('hello.env')
api_key = os.getenv("GOOGLE_API_KEY")

# Ensure the API key is correctly set
if api_key is None:
    raise ValueError("API key not found in environment variables.")

# Initialize LLM and embeddings
llm = GoogleGenerativeAI(google_api_key=api_key, model='models/text-bison-001', temperature=0.9)
instructor_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query")

vectordb_file_path = "faiss_index"

def create_vector_db():
    """
    Create a FAISS vector database from the CSV file and save it locally.
    """
    try:
        loader = CSVLoader(file_path="project.csv", source_column="States + UTs")
        data = loader.load()
        vectordb = FAISS.from_documents(documents=data, embedding=instructor_embeddings)
        vectordb.save_local(vectordb_file_path)
        print("Vector database created and saved successfully.")
    except Exception as e:
        print(f"Error creating vector database: {e}")

def get_qa_chain():
    """
    Load the FAISS vector database and create a RetrievalQA chain for question answering.
    """
    try:
        vectordb = FAISS.load_local(vectordb_file_path, instructor_embeddings, allow_dangerous_deserialization=True)
        retriever = vectordb.as_retriever(score_threshold=0.7)

        prompt_template = """
        Given the following context and a question, generate an answer based on this context only.
        In the answer try to provide as much text as possible from the "response" section in the source document context without making much changes.
        If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

        CONTEXT: {context}

        QUESTION: {question}
        Please provide a detailed and comprehensive answer that includes multiple aspects and detailed explanations where possible.
        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain_type_kwargs = {"prompt": prompt}
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            input_key="query",
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs
        )
        return chain
    except Exception as e:
        print(f"Error creating QA chain: {e}")
        return None

def evaluate_bleu(reference_answers, generated_answers):
    """
    Evaluate the BLEU score of the generated answers against reference answers.
    """
    smoothing_function = SmoothingFunction().method1
    scores = {'1-gram': [], '2-gram': [], '3-gram': []}
    
    for ref, gen in zip(reference_answers, generated_answers):
        ref_tokens = [nltk.word_tokenize(ref.lower())]
        gen_tokens = nltk.word_tokenize(gen.lower())
        
        # Calculate BLEU score for 1-gram, 2-gram, and 3-gram
        for n in range(1, 4):
            weights = [1.0 / n] * n + [0] * (4 - n)
            score = sentence_bleu(ref_tokens, gen_tokens, weights=weights, smoothing_function=smoothing_function)
            scores[f'{n}-gram'].append(score)
    
    return scores

def evaluate_rouge(reference_answers, generated_answers):
    """
    Evaluate the ROUGE scores of the generated answers against reference answers.
    """
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = {'rouge1': [], 'rouge2': [], 'rougeL': []}
    
    for ref, gen in zip(reference_answers, generated_answers):
        score = scorer.score(ref, gen)
        for key in scores:
            scores[key].append(score[key].fmeasure)
    
    return scores

if __name__ == "__main__":
    create_vector_db()
    chain = get_qa_chain()

    if chain:
        # Example questions and reference answers for BLEU and ROUGE evaluation
        questions = ["What are the spiritual practices of Assam?", "What are some places we can visit in Rajasthan to experience their spiritual practices?"]
        reference_answers = [
            "Sankirtan. Vaishnavism. Group singing, dancing, and music as meditative practices. Devotion through music.Herbal steam baths. Traditional Assamese massage. Use of local medicinal plants for healing. 1. Kamakhya Temple, Guwahati; 2. Umananda Temple, Guwahati; 3. Sivasagar Sivadol, Sivasagar; 4. Mahamaya Temple, Bongaigaon; 5. Hajo Powa Mecca, Hajo	Important religious and historical sites	Available through hotels and tourism boards	October to April	5-7 days Airport: Lokpriya Gopinath Bordoloi International Airport, Guwahati (GAU) Railway Station: Guwahati Railway Station Road	Heritage hotels in Guwahati, guest houses	Temple volunteering, cultural preservation projects	1. Lyangcha, 2. Maach Jhol, 3. Alu Pitika, 4. Masor tenga, 5. Bilahi Maas, 6. Bora Sawul, 7. Haq Maas, 8. Koldil Chicken, 9. Masor Koni, 10. Payokh, 11. Til Pitha"
            ,
            "1. Dilwara Temples, Mount Abu; 2. Birla Mandir, Jaipur; 3. Brahma Temple, Pushkar; 4. Ranakpur Jain Temple, Ranakpur; 5. Govind Dev Ji Temple, Jaipur	Prominent pilgrimage sites and ancient temples	Available through hotels and tourism boards	October to March	7-10 days	Airport: Jaipur International Airport (JAI) Railway Station: Jaipur Junction (JP) Road	 Taj Lake Palace Udaipur, The Oberoi Udaivilas Udaipur, heritage hotels in Jaipur and Jodhpur	Temple volunteering, cultural preservation projects	1. Boondi, 2. Ghevar, 3. Daal baati churma, 4. Pattor, 5. Gatta curry, 6. Churma Ladoo"
        ]

        # Generate answers
        generated_answers = [chain({"query": question})['result'] for question in questions]

        # Evaluate BLEU scores
        bleu_scores = evaluate_bleu(reference_answers, generated_answers)
        for question, gen in zip(questions, generated_answers):
            print(f"Question: {question}")
            print(f"Generated Answer: {gen}")
            print(f"BLEU Scores:")
            for ngram, scores in bleu_scores.items():
                avg_score = sum(scores) / len(scores) if scores else 0
                print(f"  {ngram}: {avg_score:.4f}")
            print()

        # Evaluate ROUGE scores
        rouge_scores = evaluate_rouge(reference_answers, generated_answers)
        for question, gen in zip(questions, generated_answers):
            print(f"Question: {question}")
            print(f"Generated Answer: {gen}")
            print(f"ROUGE Scores:")
            for metric, scores in rouge_scores.items():
                avg_score = sum(scores) / len(scores) if scores else 0
                print(f"  {metric.upper()}: {avg_score:.4f}")
            print()
