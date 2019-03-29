import requests
import os
import json
from gnews import gnewsclient

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "newsbot-32f31-b70bd494fe81.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newsbot-32f31"


# endpoint of the news API
# GNEWS_API_ENDPOINT = "https://gnewsapi.herokuapp.com"

# available news categories
news_categories = [('sports', 'sports news'), ('political', 'political news'), ('business', 'business news'), 
				   ('top stories', 'top stories news'), ('world', 'world news'), ('national', 'national news'), 
					('technology', 'technology news'), ('entertainment', 'entertainment news')]

url_news={
	'sports':"https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pKVGlnQVAB",
	'political':"https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRFZ4ZERBU0JXVnVMVWRDS0FBUAE", 
	'business':"https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pKVGlnQVAB", 
	'top stories':"https://news.google.com/", 
	'world':"https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pKVGlnQVAB", 
	'national':"https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNRE55YXpBU0FtVnVLQUFQAQ", 
	'technology':'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pKVGlnQVAB', 
	'entertainment':"https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pKVGlnQVAB"
}

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


def get_news(params):
	"""
	function to fetch news from news API
	"""
	# params['news'] = params.get('news_type', 'top stories')
	# params['news'] = params['news_type']
	url=None
	if 'news' in params:
		if params['news'] in url_news:
			url=url_news[params['news']]
		else:
			url=url_news["top stories"]
	else:
		url=url_news["top stories"]
	gnews=gnewsclient(url=url)
	# resp = requests.get(GNEWS_API_ENDPOINT, params = params)
	resp=gnews.get_news()
	return resp

def fetch_reply(query,sender_id):
	response=detect_intent_from_text(query,sender_id)
	intent_name=response.intent.display_name
	reply={}
	if intent_name=='show_news':
		params=response.parameters
		parameters={}
		parameters['news']=params['news_type']
		# reply['type'] = 'news'

		parameters['sender_id'] = sender_id
		
		articles = get_news(parameters)
		return articles,2
	else:
		return response.fulfillment_text,1

		# create generic template
		# news_elements = []

		# for article in articles:
		# 	element = {}
		# 	element['title'] = article['title']
		# 	element['item_url'] = article['link']
		# 	element['image_url'] = article['img']
		# 	element['buttons'] = [{
		# 		"type":"web_url",
		# 		"title":"Read more",
		# 		"url":article['link']}]
		# 	news_elements.append(element)

		# reply['data'] = articles
	

