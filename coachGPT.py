from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests



app = Flask(__name__)

chat_history = []

def generate_answer(question):
    url = 'https://api.writesonic.com/v1/botsonic/botsonic/generate/5e1a2fdd-d763-4ceb-a688-c8da7122f8ad'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'python-requests/2.28.1',
        'accept': 'application/json',
        'token': os.getenv('BOTSONIC_TOKEN'),
    }
    data = {
        'question': question,
        'chat_history': chat_history,
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        if isinstance(response_data, list) and len(response_data) > 0:
            message = response_data[0]['data'].get('answer', '')
            chat_history.append({
                'message': question,
                'sent': True
            })
            chat_history.append({
                'message': message,
                'sent': False
            })
        else:
            message = 'No answer found.'
    else:
        message = 'An error occurred while generating the answer.'
    
    return message

@app.route('/coachgpt', methods=['POST'])
def chatgpt():
    incoming_question = request.values.get('Body', '').lower()
    message = generate_answer(incoming_question)
    
    bot_resp = MessagingResponse()
    bot_resp.message(message)
    
    return str(bot_resp)



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5000)
