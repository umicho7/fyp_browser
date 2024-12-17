from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS
from dotenv import load_dotenv
import openai

load_dotenv()

app=Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}})


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/search', methods=['GET'])
def search():
    query=request.args.get('q')
    if not query:
        return jsonify({'error':'No query provided'}), 400
    
    search_url='https://www.googleapis.com/customsearch/v1'
    params = {
        'key':GOOGLE_API_KEY,
        'cx':GOOGLE_CSE_ID,
        'q':query
    }
    
    response = requests.get(search_url, params=params)
    
    if response.status_code!=200:
        return jsonify({'error':'Failed to fetch search results'}), response.status_code
    
    data= response.json()
    
    results=[]
    for item in data.get('items',[]):
        results.append(
            {
                'title':item.get('title'),
                'link':item.get('link'),
                'snippet':item.get('snippet')
            }
        )
    return jsonify({'results': results})
@app.route('/chat', methods=['POST'])
def chat():
    # Extract the user's message from the request
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Make a request to the OpenAI ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Update to "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        # Extract the chatbot's response
        bot_message = response.choices[0].message['content']
        return jsonify({'bot_message': bot_message})
    except openai.error.AuthenticationError:
        return jsonify({'error': 'Invalid API Key. Please check your configuration.'}), 500
    except openai.error.OpenAIError as e:
        return jsonify({'error': f'OpenAI API Error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)