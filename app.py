from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_frozen import Freezer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='gevent')
freezer = Freezer(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        username = users[request.sid]
        del users[request.sid]
        emit('message', f'{username} has left the chat room.', broadcast=True)
        print(f'{username} has disconnected')

@socketio.on('join')
def handle_join(username):
    users[request.sid] = username
    emit('message', f'{username} has joined the chat room.', broadcast=True)
    print(f'{username} has connected')

@socketio.on('message')
def handle_message(data):
    if request.sid in users:
        username = users[request.sid]
        print(f'received message from {username}: {data}')
        emit('message', f'{username}: {data}', broadcast=True)

if __name__ == '__main__':
    freezer.freeze()