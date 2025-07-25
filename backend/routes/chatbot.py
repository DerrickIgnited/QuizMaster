import os
from flask import Blueprint, request, jsonify, current_app
import requests
import logging
from .utils import cache_response

chatbot_bp = Blueprint('chatbot', __name__)

def create_prompt(user_message):
    prompt = f"""
You are Quiz Master AI assistant. Help the user with quiz-related questions and provide clear, concise answers.
Respond in markdown format to allow rich text formatting.
User: {user_message}
AI:
"""
    return prompt

@chatbot_bp.route('/chat', methods=['POST'])
@cache_response('chatbot_chat', timeout=60)
def chat():
    data = request.json
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    prompt = create_prompt(user_message)

    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        current_app.logger.error('GEMINI_API_KEY not configured')
        return jsonify({'error': 'API key not configured'}), 500

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': prompt,
        'max_tokens': 150,
        'temperature': 0.7,
        'model': 'gemini-1'  
    }

    try:
        gemini_api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'

        body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": user_message
                        }
                    ]
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': api_key
        }

        response = requests.post(gemini_api_url, json=body, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        ai_text = ""
        if "candidates" in result and len(result["candidates"]) > 0:
            content = result["candidates"][0].get("content", "")
            if isinstance(content, dict):
                parts = content.get('parts', [])
                texts = []
                for part in parts:
                    text = part.get('text', '')
                    if text:
                        texts.append(text)
                ai_text = "\\n".join(texts).strip()
            else:
                ai_text = content.strip()
        return jsonify({'response': ai_text})
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f'Gemini API call failed: {e}')
        return jsonify({'error': 'Failed to get response from AI service'}), 500
