# generic libraries
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room

# customize libraries
# import webrtc

# configurations
config = {
    'debug_mode': False
}

# initialize flask web
app = Flask(__name__)
app.secret_key = 'random secret key!'
socketio = SocketIO(app, cors_allowed_origins="*")

# event handler for the join event 
@socketio.on('join')
def join(message):
    username = message['username']
    room = message['room']
    join_room(room)
    print('RoomEvent: {} has joined the room {}\n'.format(username, room))
    emit('ready', {username: username}, to=room, skip_sid=request.sid)

# event handler for the data event
@socketio.on('data')
def transfer_data(message):
    username = message['username']
    room = message['room']
    data = message['data']
    print('DataEvent: {} has sent the data:\n {}\n'.format(username, data))
    emit('data', data, to=room, skip_sid=request.sid)

# error handler
@socketio.on_error_default
def default_error_handler(e):
    print("Error: {}".format(e))
    socketio.stop()

'''
# home page
@app.route("/")
def homepage():
    return "<p>Welcome to WebRTC website!</p>"

@app.route("/videocall")
def videocall():
    return "<p>This is videocall page!</p>"
'''

if __name__=='__main__':
    socketio.run(app, host="0.0.0.0", port=9000)
    # app.run(host='0.0.0.0', debug=config['debug_mode'])
