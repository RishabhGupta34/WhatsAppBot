from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse,Message
from utils import fetch_reply
import time
import os
app = Flask(__name__, static_url_path='')

@app.route("/")
def hello():
    return "Hello, World!"

port = int(os.getenv("VCAP_APP_PORT"))

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    start=time.time()
    msg = request.form.get('Body')
    phone_no=request.form.get('From')
    # Create reply
    reply,opt=fetch_reply(msg,phone_no)
    if opt==1:
    	resp = MessagingResponse()
    	resp.message(reply)
    else:
    	# resp = MessagingResponse(to=phone_no)
    	# resp.message("Showing the news")
    	resp = MessagingResponse()
    	print(reply)
    	for i in reply:
    		article=Message()
    		article.body(i['title']+"("+i['releasedAt']+") Link: "+i['link'])
    		# article.media(i['img'])
    		resp.append(article)
    print(time.time()-start)
    return str(resp)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
