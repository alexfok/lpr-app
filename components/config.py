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
# Nasty hack for Heroku environment due to Windows shell bug - unable to perform
#   heroku config:set TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/4.00/tessdata
#if 'heroku' in os.environ.get('PATH'):
if 'DYNO' in os.environ:
    os.environ['TESSDATA_PREFIX'] = '/app/.apt/usr/share/tesseract-ocr/4.00/tessdata'
else:
    os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"
#os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'
#    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
logger.debug("config:TESSDATA_PREFIX '{}'\n\n PATH:\n '{}'".format(os.environ.get('TESSDATA_PREFIX'), os.environ.get('PATH')))
#
#     os.environ['TESSDATA_PREFIX'] = 'C:\Program Files\Tesseract-OCR\tessdata'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    datetime.now().strftime(DATE_FORMAT)
    return value.strftime(format)
