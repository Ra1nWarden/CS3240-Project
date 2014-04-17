import os
from flask import Flask, request, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/zihaowang/test/'

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def sync_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return make_response()
    if request.method == 'DELETE':
        filename = request.args['file']
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return make_response()
    if request.method == 'GET':
        filename = os.path.join(app.config['UPLOAD_FOLDER'], request.args['file'])
        print filename
        resp = send_file(filename, as_attachment=True)
        return resp

@app.route('/query', methods=['GET'])
def respond_requests():
    if request.method == 'GET':
        file_info = request.args
        server_files = os.listdir(app.config['UPLOAD_FOLDER'])
        server_info = {}
        for each in server_files:
            server_info[each] = os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], each))
        uploadneed = []
        downloadneed = []
        for each in file_info:
            if not each in server_info:
                uploadneed.append(each)
            else:
                if server_info[each] > file_info[each]:
                    downloadneed.append(each)
                else:
                    uploadneed.append(each)
        for each in server_info:
            if not each in file_info:
                downloadneed.append(each)
        resp = jsonify(upload=uploadneed, download=downloadneed)
        return resp

if __name__ == '__main__':
    app.run()
