from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import glob
from werkzeug.utils import secure_filename
from components import utils
from components.utils import init_logger

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = "secret key"
#app = Flask(__name__, static_folder=os.path.join(os.path.pardir, '..', 'static'))

app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 # 8 MB

PICTURES_FOLDER = os.path.join('static', 'pictures_photo')
app.config['UPLOAD_FOLDER'] = PICTURES_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../static/test_pictures.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# DATE_FORMAT is the date format in the files. Watch out - changing this requires server cleanup
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logger = init_logger()
import os
if 'heroku' in os.environ.get('PATH')):
    os.environ['TESSDATA_PREFIX'] = '/app/.apt/usr/share/tesseract-ocr/4.00/tessdata'
logger.debug("config:TESSDATA_PREFIX '{}'\n\n PATH:\n '{}'".format(os.environ.get('TESSDATA_PREFIX'), os.environ.get('PATH')))

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    datetime.now().strftime(DATE_FORMAT)
    return value.strftime(format)
