UPLOAD_FOLDER = '/home/zihao/Dropbox/Documents/UVa/Spring 2014/CS 3240/CS3240-Project/server_folder/'
SECRET_KEY = 'you-will-never-guess'
CSRF_ENABLED = True

import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
