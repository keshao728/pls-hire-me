from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pickle
import requests
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI
from multiprocessing import Process, Manager
import uuid
import time
import nltk

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5003", "http://0.0.0.0:5003"]}})

# Create a shared list for tasks in progress
manager = Manager()
tasks_in_progress = manager.list()

# Create a shared dictionary for completed tasks
completed_tasks = manager.dict()

# Perform a Google search to retrieve relevant site information
def google_search(query, api_key, cx_id, **kwargs):
    """
    Used Google Custom Search API to perform targeted searches.
    Fetches search results and returns a list of relevant search items.
    """

    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': api_key,
        'cx': cx_id,
        'q': query,
        'start': 1,
        'num': 3
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        raise Exception('Google Search API request failed with status code {}'.format(response.status_code))

    if 'items' in data:
        return data['items']
    else:
        return []

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')

@app.route('/', methods=['GET'])
def index():
    return "Hello World!"

# Set up API endpoint for offloading processing
@app.route('/process', methods=['POST'])
def process_data():
    global tasks_in_progress, completed_tasks

    request_data = request.get_json()

    # Download and install NLTK data if not already available
    nltk.download('punkt', download_dir='/root/nltk_data')
    nltk.download('averaged_perceptron_tagger', download_dir='/root/nltk_data')

    if 'site_names' not in request_data:
        return make_response(jsonify({'error': 'Missing site_names parameter'}), 400)

    queries = [
        "What is the main product or service of {}?",
        "What is the business strategy of {}?",
        "How is {} perceived in the market?",
    ]

    # Load essential API keys from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    cx_id = os.getenv("CX_ID")

    os.environ["OPENAI_API_KEY"] = openai_api_key

    task_id = generate_unique_id()
    p = Process(target=process_task, args=(task_id, request_data.get('site_names'), queries, google_api_key, cx_id, tasks_in_progress))
    p.start()

    tasks_in_progress.append(task_id)

    return make_response(jsonify({'task_id': task_id}), 200)

def process_task(task_id, site_names, queries, google_api_key, cx_id, tasks_in_progress):
    results = []  # Initialize results as an empty list

    for site_name in site_names:
        # Perform a targeted Google search for each site name
        search_results = google_search(site_name, google_api_key, cx_id, num=3)
        urls = [result['link'] for result in search_results]

        loaders = UnstructuredURLLoader(urls=urls)
        loaded_data = loaders.load()

        # Split loaded data into manageable chunks for processing
        text_splitter = CharacterTextSplitter(
            separator='.', chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(loaded_data)

        # Convert text chunks into vector representations for semantic analysis
        embeddings = OpenAIEmbeddings()
        vectorStore_openAI = FAISS.from_documents(docs, embeddings)

        # Serialize and persist vector store for future use
        with open("faiss_store_openai.pkl", "wb") as f:
            pickle.dump(vectorStore_openAI, f)

        # Load the serialized vector store from the file
        with open("faiss_store_openai.pkl", "rb") as f:
            VectorStore = pickle.load(f)

        # Utilize advanced NLP models for generating informative reports
        llm = OpenAI(temperature=0)
        chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=VectorStore.as_retriever())

        site_report = {}
        for query in queries:
            # Format the query with the site name to extract relevant insights
            full_query = query.format(site_name)

            # Introduce a delay before making each API request to rate limit the requests
            time.sleep(2)  # Adjust the delay as needed

            # Utilize the chain to obtain targeted responses
            result = chain({"question": full_query}, return_only_outputs=True)

            # Store the results in a report dictionary
            site_report[full_query] = result
        results.append(site_report)

    tasks_in_progress.remove(task_id)
    completed_tasks[task_id] = results

    return

@app.route('/status/<task_id>', methods=['GET'])
def check_status(task_id):
    global tasks_in_progress, completed_tasks 

    if task_id in tasks_in_progress:
        return make_response(jsonify({'status': 'Processing'}), 200)
    elif task_id in completed_tasks:
        results = completed_tasks[task_id]
        return make_response(jsonify({'status': 'Completed', 'results': results}), 200)
    else:
        return make_response(jsonify({'status': 'Invalid task ID'}), 404)

def generate_unique_id():
    # Generate a unique ID for each task
    return str(uuid.uuid4())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5003)))
