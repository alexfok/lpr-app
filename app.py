from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import glob
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 # 8 MB

PICTURES_FOLDER = os.path.join('static', 'pictures_photo')
app.config['UPLOAD_FOLDER'] = PICTURES_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_pictures.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Pictures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    large_picture = ""
    small_pictures = []

    def __repr__(self):
        return '<Pictures %r>' % self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # New picture upload
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No image selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #print('upload_image filename: ' + filename)
                name = os.path.splitext(filename)[0]
                new_picture = Pictures(name=name)
                db.session.add(new_picture)
                db.session.commit()
                flash('Image successfully uploaded and displayed')
                return redirect(request.url)
            else:
                flash('Allowed image types are -> png, jpg, jpeg, gif')
                return redirect(request.url)
            return redirect(request.url)
        except:
            flash('There was a problem adding new stuff.')
            return redirect(request.url)
#            return "There was a problem adding new stuff."
    else:
        # GET - render existing pictures
        car_pictures = Pictures.query.order_by(Pictures.created_at).all()
        for car_picture in car_pictures:
#            car_picture.large_picture = os.path.join(app.config['UPLOAD_FOLDER'], car_picture.name + ".jpg")
#            for small_picture in glob.glob('static/pictures_photo/' + name + '*'):
            pictures_list = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], car_picture.name + "*"))
            for picture_path in pictures_list:
                small_picture_name = os.path.basename(picture_path)
                small_picture_name = os.path.splitext(small_picture_name)[0]
                if small_picture_name == car_picture.name:
                    car_picture.large_picture = picture_path
                    pictures_list.remove(picture_path)
            car_picture.small_pictures = pictures_list
#            print("car_picture.large_picture: {}", car_picture.large_picture)
#            print("car_picture.small_pictures: {}", car_picture.small_pictures)
        return render_template('index.html', car_pictures=car_pictures)


@app.route('/delete/<int:id>')
def delete(id):
    car_picture = Pictures.query.get_or_404(id)

    try:
        db.session.delete(car_picture)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting data."


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    car_picture = Pictures.query.get_or_404(id)

    if request.method == 'POST':
        car_picture.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
        title = "Update Data"
        return render_template('update.html', title=title, car_picture=car_picture)


if __name__ == '__main__':
    app.run(debug=True)
