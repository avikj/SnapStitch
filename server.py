from flask import Flask, request, jsonify
import time
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS= set(["mp4"])

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
	return "A happy little HTML page"

@app.route('/upload', methods=["POST"])
def upload():
	starttime = time.time()
	groupid = None
	if request.args.get('groupid'):
		groupid = request.args.get('groupid')
	else:
		groupid = time.time()
	f = request.files.getlist('videoupload')
	savelocation = './videos/{0}'.format(groupid)
	if not os.path.exists(savelocation):
		os.makedirs(savelocation)
	for file in f:
		file.save(os.path.join(savelocation,file.filename))
	endtime = time.time()
	return jsonify(groupid=groupid)

if __name__ == '__main__':
	app.run(debug=True)

