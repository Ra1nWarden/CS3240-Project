import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/zihaowang/test/'

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def sync_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if request.method == 'DELETE':
        print "here"
        filename = request.args['file']
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == '__main__':
    app.run()

