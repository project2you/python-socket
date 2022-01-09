import os
from flask import Flask, render_template, session, copy_current_request_context , request , jsonify
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock

from tqdm import tqdm
from time import sleep
import psutil
import socket


async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]
  
@app.route('/')
def index():
    print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    return render_template('index.html', async_mode=socket_.async_mode)

@socket_.on('my_event', namespace='/test')
def test_message(message):
        while True :
            session['cpu']= psutil.cpu_percent(4)
            session['receive_count'] = psutil.virtual_memory()[2]
            session['host'] = getNetworkIp()
            print(psutil.cpu_percent(4))
            session['client_ip'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            print(session['client_ip'])
            emit('my_response', {'data': message['data'], 'count': session['receive_count'] , 'cpu': session['cpu'] , 'host' : session['host'] ,>
            sleep(100)

@socket_.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = vcc=psutil.cpu_count()
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)
                                 
@socket_.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)

if __name__ == '__main__':
    print (getNetworkIp())
    print(psutil.disk_usage(os.sep))
    print(psutil.disk_usage(os.sep).percent)
    socket_.run(app, host='0.0.0.0', debug=True)
