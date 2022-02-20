from flask import Flask, render_template, request
from flask_socketio import *
import json
import os


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/signals', methods=['GET','POST'])
def signals():
    """Return signals."""
    if request.method == 'POST':
        
        test_bot = Bot(['AAPL','AMD','TSLA','QQQ','NVDA','PYPL','F','SNAP'])
        test_bot.setup()
        test_bot.get_live_price_data()       

# SocketIO Events
@socketio.on('connect')
def connected():
    print('Connected')

@socketio.on('disconnect')
def disconnected():
    print('Disconnected')

@socketio.on('CompaniesAdded')
def companies_added(message):
    test_bot = Bot(message)
    test_bot.setup()
    signal_info = test_bot.get_live_price_data()  
    print('companies Added')
    

if __name__ == '__main__':
    socketio.run(app, debug=True)
