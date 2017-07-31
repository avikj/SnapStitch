from flask import Flask, request, jsonify, render_template, abort, send_from_directory
from flask_cors import CORS, cross_origin
import time
import os
import random
import threading
from video_processing import main as video_processing

app = Flask(__name__)

ALLOWED_EXTENSIONS= set(["mp4"])

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/results/<filename>')
def results(filename):
    if not os.path.isfile(os.path.join('results', 'finished_'+filename[:filename.rindex('.')]+'.txt')):
        abort(404)
        return
    return send_from_directory('results',filename)

@app.route('/<groupid>')
def index(groupid):
	return render_template('index.html', groupid = groupid)

@app.route('/file/<groupid>')
def file(groupid):
	if os.path.isfile(os.path.join(os.getcwd(),'results/{0}.m4v'.format(groupid))):
		return jsonify(groupid=groupid)
	else:
		abort(404)

@app.route('/add')
def add():
  return render_template('add.html')

@app.route('/loading/<groupid>')
def loading(groupid):
	return render_template('loading.html', groupid=groupid)

@app.route('/upload', methods=["POST"])
def upload():
	starttime = time.time()
	groupid = None
	if request.args.get('groupid'):
		groupid = request.args.get('groupid')
	else:
		groupid = (int(time.time()) * 1000) + random.randint(0,999)
	f = request.files.getlist('vidfiles')
	savelocation = './videos/{0}'.format(groupid)
	if not os.path.exists(savelocation):
		os.makedirs(savelocation)
	for file in f:
		file.save(os.path.join(savelocation,file.filename.lower()))
	endtime = time.time()
	totaltime = endtime-starttime
	thread = threading.Thread(target=video_processing, args=(str(groupid),))
	thread.start()
	return jsonify(groupid=groupid, time=totaltime)

if __name__ == '__main__':
	app.run(debug=True, threaded=True, host="0.0.0.0", port=6006)
