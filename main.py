from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
socketIO = SocketIO(app)

messages_by_rooms = dict()


@app.route('/')
def hello_world():
    return render_template('index.html', messages_by_rooms=messages_by_rooms)


@socketIO.on('join')
def on_join(room):
    join_room(room)
    send('Someone has entered the room ' + room, to=room)


@socketIO.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    send('Someone has left the room ' + room, to=room)

@socketIO.event
def add_message(json):
    room = json['room']
    text = json['text']
    if room not in messages_by_rooms:
        messages_by_rooms[room] = []
    messages_by_rooms[room].append(text)
    emit('new_message', json, to=room)


if __name__ == '__main__':
    app.run()
    socketIO.run(app)
