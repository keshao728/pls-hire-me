from flask import Flask, request, jsonify, make_response, send_from_directory
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
from googleapiclient.discovery import build

load_dotenv()

# app = Flask(__name__, static_folder='static')
app = Flask(__name__, static_folder='static', static_url_path='/static')

CORS(app)

# Serve React app as static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
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
        'num': 5
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        print(response)
        raise Exception('Google Search API request failed with status code {}'.format(
            response.status_code))

    if 'items' in data:
        return data['items']
    else:
        return []

# Set up API endpoint
@app.route('/process', methods=['POST'])
def process_data():
    request_data = request.get_json()

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

    results = []
    for site_name in request_data.get('site_names'):
        # Perform a targeted Google search for each site name
        search_results = google_search(site_name, google_api_key, cx_id, num=3)
        urls = [result['link'] for result in search_results]
        loaders = UnstructuredURLLoader(urls=urls)
        loaded_data = loaders.load()

        # Split loaded data into manageable chunks for processing
        text_splitter = CharacterTextSplitter(
            separator='\n', chunk_size=1000, chunk_overlap=200)
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
        chain = RetrievalQAWithSourcesChain.from_llm(
            llm=llm, retriever=VectorStore.as_retriever())

        site_report = {}
        for query in queries:
            # Format the query with the site name to extract relevant insights
            full_query = query.format(site_name)

            # Utilize the chain to obtain targeted responses
            result = chain({"question": full_query}, return_only_outputs=True)

             # Store the results in a report dictionary
            site_report[full_query] = result
        results.append(site_report)
        print("results:", results)

    return make_response(jsonify({'results': results}), 200)


if __name__ == '__main__':
    app.run(port=5010)
