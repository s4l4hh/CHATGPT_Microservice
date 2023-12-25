# app.py
import os
import csv
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Question not provided'}), 400

    try:
        answer = query_chatgpt(question)
        save_to_csv(question, answer)
        return jsonify({'question': question, 'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def query_chatgpt(question):
    api_key = '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'
    api_url = 'https://api.openai.com/v1/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': 'text-davinci-003',
        'prompt': question,
        'max_tokens': 4000
    }

    response = requests.post(api_url, json=data, headers=headers)
    response.raise_for_status()

    result = response.json()
    return result['choices'][0]['text'].strip()

def save_to_csv(question, answer):
    csv_path = '/app/data/questions_and_answers.csv'

    # Check if the CSV file already exists
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='') as csvfile:
            fieldnames = ['Question', 'Answer']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    # Append the new question and answer to the CSV file
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([question, answer])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
