from flask import Blueprint, render_template, request, jsonify
from .brain import Brain
import uuid
from datetime import datetime
import json

main_bp = Blueprint('main', __name__)
brain = Brain()

# ... (State Management code remains same) ...
# Structure: {user_addr: {'request_count': int, 'last_topic': str, 'last_intent': str}}
user_session_data = {}
chat_sessions = {}

def get_user_id():
    return request.remote_addr

def get_user_session(user_id):
    if user_id not in chat_sessions:
        chat_sessions[user_id] = {'chats': {}, 'current_chat_id': None}
        create_new_chat(user_id)
    return chat_sessions[user_id]

def create_new_chat(user_id):
    session = chat_sessions[user_id]
    chat_id = str(uuid.uuid4())
    session['chats'][chat_id] = {
        'title': 'Nouvelle conversation',
        'messages': [],
        'context': [],
        'created_at': datetime.now().isoformat()
    }
    session['current_chat_id'] = chat_id
    if user_id not in user_session_data:
        user_session_data[user_id] = {'request_count': 0, 'last_topic': None, 'last_intent': None}
    return chat_id

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    user_id = get_user_id()
    
    if request.headers.get('X-Test-User'):
        user_id = f"test-{request.headers.get('X-Test-User')}"

    session = get_user_session(user_id)
    if not session['current_chat_id'] or session['current_chat_id'] not in session['chats']:
        create_new_chat(user_id)
        
    chat_id = session['current_chat_id']
    chat_data = session['chats'][chat_id]

    if not chat_data['messages']:
        chat_data['title'] = (user_input[:30] + '...') if len(user_input) > 30 else user_input

    chat_data['messages'].append({'sender': 'user', 'content': user_input})
    
    if user_id not in user_session_data:
        user_session_data[user_id] = {'request_count': 0, 'last_topic': None, 'last_intent': None}
    user_session_data[user_id]['request_count'] += 1
    
    response = brain.generate_response(user_input, chat_data['context'], user_session_data[user_id]['request_count'])
    
    chat_data['messages'].append({'sender': 'bot', 'content': response})
    
    return jsonify({'response': response, 'chatId': chat_id, 'title': chat_data['title']})

@main_bp.route('/reset', methods=['POST'])
def reset():
    user_id = get_user_id()
    # Create a new chat instead of wiping everything
    new_chat_id = create_new_chat(user_id)
    return jsonify({'status': 'reset', 'chatId': new_chat_id})

@main_bp.route('/history', methods=['GET'])
def get_history():
    user_id = get_user_id()
    session = get_user_session(user_id)
    chats = []
    for chat_id, data in session['chats'].items():
        chats.append({
            'id': chat_id,
            'title': data['title'],
            'created_at': data.get('created_at', '')
        })
    # Sort by date new to old
    chats.sort(key=lambda x: x['created_at'], reverse=True)
    return jsonify({'history': chats, 'currentChatId': session['current_chat_id']})

@main_bp.route('/load_chat/<chat_id>', methods=['GET'])
def load_chat(chat_id):
    user_id = get_user_id()
    session = get_user_session(user_id)
    if chat_id in session['chats']:
        session['current_chat_id'] = chat_id
        return jsonify({'messages': session['chats'][chat_id]['messages']})
    else:
        return jsonify({'error': 'Chat not found'}), 404
