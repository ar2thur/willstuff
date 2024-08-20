from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins='*')

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect(sid):
    if sid in users:
        username = users[sid]
        del users[sid]
        emit('message', f'{username} has left the chat room.', broadcast=True)
        print(f'{username} has disconnected')

@socketio.on('join')
def handle_join(username, sid=None):
    if sid is None:
        sid = request.sid
    users[sid] = username
    emit('message', f'{username} has joined the chat room.', broadcast=True)
    print(f'{username} has connected')

@socketio.on('message')
def handle_message(data, sid=None):
    if sid is None:
        sid = request.sid
    if sid in users:
        username = users[sid]
        print(f'received message from {username}: {data}')
        emit('message', f'{username}: {data}', broadcast=True)

if __name__ == '__main__':
    socketio.run(app)