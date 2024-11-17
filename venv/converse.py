import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from newsapi import NewsApiClient
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

news = NewsApiClient(api_key='da8ad38bdd82455681188a4a3a506fd8')

@app.route('/')
def home():
    return render_template('index.html')

load_dotenv()

# Put your AWS credentials in a .env file
access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

client = boto3.client(
    service_name="bedrock-runtime",
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    region_name="us-west-2",
)

# The model ID for the model you want to use
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

# SUMMARY OF ORIGINAL DOCUMENT
@app.route('/summarize', methods=['POST'])
def summarize():
    input = request.form['user_input']

    user_message = "Tell me about this document's most important key points, and a short paragraph summary.\n"
    user_message += "Do not include any leading or ending points. Only include the key points and summary.\n"
    user_message += input

    summaryConversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    summary_output = ''

    try:
        streaming_response = client.converse_stream(
            modelId=model_id,
            messages=summaryConversation,
            inferenceConfig={"maxTokens": 4095, "temperature": 0.3, "topP": 0.9},
        )

        # Extract and print the streamed response text in real-time.
        for chunk in streaming_response["stream"]:
            if "contentBlockDelta" in chunk:
                text = chunk["contentBlockDelta"]["delta"]["text"]
                summary_output += chunk["contentBlockDelta"]["delta"]["text"]
        summary_output += '\n'
        return jsonify(summary_output.replace("\n", "<br>"))

    except (ClientError, Exception) as e:
        return(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")


# NEWS KEYWORDS OF SUMMARY
@app.route('/newskeywords', methods=['POST'])
def newskeywords():
    input = request.form['user_input']

    keyword_getter = "Give me 4 key words about this passage (only the keywords, don't include anything (like 'keywords:') in the front or back), in one line, separated by ONLY spaces and a single commas\n"
    keyword_getter += input
    keyword_output = ""

    keywordConversation = [
        {
            "role": "user",
            "content": [{"text": keyword_getter}],
        }
    ]

    try:
        streaming_response = client.converse_stream(
            modelId=model_id,
            messages=keywordConversation,
            inferenceConfig={"maxTokens": 75, "temperature": 0.7, "topP": 0.9},
        )

        # Extract and print the streamed response text in real-time.
        for chunk in streaming_response["stream"]:
            if "contentBlockDelta" in chunk:
                text = chunk["contentBlockDelta"]["delta"]["text"]
                keyword_output += chunk["contentBlockDelta"]["delta"]["text"]

        linkArr = getNews(keyword_output)
        i = 0
        returnString = ''
        for arr in linkArr:
            for item in arr:
                if i % 2 == 1:
                    returnString += f'<a href="{item}" target="_blank">{item}</a>\n'
                else:
                    returnString += item + "\n"
                i += 1
            returnString += "\n"

        return returnString.replace("\n", "<br>")

    except (ClientError, Exception) as e:
        return(f"Cannot find a related article.....")

def getNews(keywords):
    topics = keywords
    s = None
    d = None
    start = '2024-10-17'
    end = '2024-11-15'
    lang = 'en'
    sort = 'relevancy'
    p = None
    all_articles = news.get_everything(q = topics,
                                sources = s,
                                domains = d,
                                from_param = start,
                                to = end,
                                language = lang,
                                sort_by = sort,
                                page = p)

    total_results = all_articles['totalResults']
    result_string = ""
    source1 = []
    source2 = []
    source3 = []

    for source in all_articles['articles']:
        if source1 == []:
            source1.append(source['title'])
            source1.append(source['url'])
        elif source2 == []:
            source2.append(source['title'])
            source2.append(source['url'])
        elif source3 == []:
            source3.append(source['title'])
            source3.append(source['url'])
        else:
            return [source1, source2, source3]
        

@app.route('/researchkeywords', methods=['POST'])
def researchkeywords():
    input = request.form['user_input']

    keyword_getter = "Give me 4 key words about this passage (only the keywords, don't include anything (like 'keywords:') in the front or back), in one line, separated by ONLY spaces and a single commas\n"
    keyword_getter += input
    keyword_output = ""

    keywordConversation = [
        {
            "role": "user",
            "content": [{"text": keyword_getter}],
        }
    ]

    try:
        streaming_response = client.converse_stream(
            modelId=model_id,
            messages=keywordConversation,
            inferenceConfig={"maxTokens": 75, "temperature": 0.5, "topP": 0.9},
        )

        # Extract and print the streamed response text in real-time.
        for chunk in streaming_response["stream"]:
            if "contentBlockDelta" in chunk:
                text = chunk["contentBlockDelta"]["delta"]["text"]
                keyword_output += chunk["contentBlockDelta"]["delta"]["text"]

        linkArr = getPapers(keyword_output)
        returnString = ''
        for item in linkArr:
            returnString += item['title'] + "\n"
            returnString += f'<a href="{item['link']}" target="_blank">{item['link']}</a>\n'
            returnString += "\n"

        return returnString.replace("\n", "<br>")

    except (ClientError, Exception) as e:
        return(f"Cannot find a related research paper.....")

def getPapers(keywords, max_results=3):
    # Base URL for arXiv API
    base_url = "http://export.arxiv.org/api/query?"

    # Construct the query with the provided keywords
    search_query = f"search_query={keywords}"  # For example, 'machine learning'
    start_index = 0
    max_results = max_results

    # URL with search query and result limits
    url = f"{base_url}{search_query}&start={start_index}&max_results={max_results}"

    # Send the request to the arXiv API
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the XML response
        root = ET.fromstring(response.content)
        entries = root.findall("{http://www.w3.org/2005/Atom}entry")

        papers = []
        for entry in entries:
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            author_list = entry.findall("{http://www.w3.org/2005/Atom}author")
            authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in author_list]
            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
            arxiv_id = entry.find("{http://www.w3.org/2005/Atom}id").text  # This is the arXiv ID

            # Format the arXiv link
            arxiv_link = arxiv_id.replace("http://arxiv.org/abs/", "https://arxiv.org/abs/")

            papers.append({
                "title": title,
                "authors": authors,
                "summary": summary,
                "link": arxiv_link
            })

        return papers
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)