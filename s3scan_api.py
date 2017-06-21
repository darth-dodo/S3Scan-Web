from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import s3scan
from threading import Thread


app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
	return render_template('index.html')


# @app.route('/api')
# def api():
# 	url = request.args.get('url')
# 	if url:
# 		return url
# 	else:
# 		return "lol"

def printSocket(text, color):
	emit('data', {'data': text, 'color': color})
	s3scan.printScreen(text, color)


@socketio.on('url', namespace='/test')
def receive_url(data):
	try:
		# s3scan.initiator(data['url'])
		# emit('data', {'data': 'Abhishek', 'age': 21})
		thread = Thread(target=s3scan.initiator, args=(str(data['url'])))
		thread.start()

	# TODO this needs to go
	except Exception:
		emit('data', {'data': Exception})


@socketio.on('disconnect')
def disconnect():
	# need to do some cleanup here
	pass

if __name__ == '__main__':
	socketio.run(app)
