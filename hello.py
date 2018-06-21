from pocket import Pocket
import spacy
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import random 

p = Pocket(
consumer_key='73820-b7626621174f19626b4f04fe',
access_token='9bbd62c8-8fa2-f1ce-df16-c1d7c9'
)

def get_articles():

	api_call = p.get(contentType='article')
	articles = api_call[0]['list']
	article_info = {}

	for i in articles:
		article_info[articles[i]['resolved_url']] = [ articles[i]['given_title'], articles[i]['excerpt'] ]
	return article_info


def get_entities(article_info):

	nlp = spacy.load('en')
	article_entities = {'Default': []}

	for i in article_info:
	    doc = " ".join(article_info[i])
	    entities = nlp(doc)
	    if len(list(entities.ents)) == 0:
	        article_entities['Default'].append(i)
	        continue
	    for j in list(entities.ents):
	        try:
	            article_entities[str(j).lower()].append(i)
	        except:
	            article_entities[str(j).lower()] = [i]
	return article_entities


app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
	current_article_set = get_articles()
	article_entities = get_entities(current_article_set)

	body = request.values.get('Body', None)


	if len(body) == 0:
 		article = article_entities['Default'][random.randint(0,len(article_entities['Default']))]
	else:
		try:
			article = article_entities[body.lower()][random.randint(0, body.lower())]
		except: 
			article = article_entities['Default'][random.randint(0, len(article_entities['Default']))]

	resp = MessagingResponse()

	resp.message(article)

	return str(resp)

if __name__ == "__main__":
    app.run(debug=True)