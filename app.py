from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import glob
import logging
from werkzeug.utils import secure_filename

from components.config import db, app, logger, allowed_file, datetimeformat, PICTURES_FOLDER, ALLOWED_EXTENSIONS, DATE_FORMAT
import components.lpr_eng

from components.lpr_eng import PictureWrapper, invoke_lpr_eng

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            logger.debug("POST request.url:'{}', request.files['file']: '{}'".format(request.url, request.files['file']))
            # New picture upload
            if 'file' not in request.files:
                flash('No file part')
                logger.debug("No file part")
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No image selected for uploading')
                logger.debug("No image selected for uploading")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                picture_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(picture_path)
                #print('upload_image filename: ' + filename)
                name = os.path.splitext(filename)[0]
#                new_picture = PictureWrapper(name = name, picture_path = picture_path)
                # invoke lpr_engine and save small_pictures list and OCR text
                logger.debug("Calling invoke_lpr_eng for picture_path:'{}'".format(picture_path))
                invoke_lpr_eng(name = name, picture_path = picture_path)
#                new_picture.invoke_lpr_eng()
                flash('Image successfully uploaded and displayed')
                logger.debug("Image successfully uploaded and displayed".format(name, picture_path))
                return redirect(request.url)
            else:
                flash('Allowed image types are -> png, jpg, jpeg, gif')
                logger.error("Allowed image types are -> png, jpg, jpeg, gif: '{}'".format(file.filename))
                return redirect(request.url)
            return redirect(request.url)
        except:
            flash('There was a problem adding new picture.')
            logger.error("There was a problem adding new picture.")
            return redirect(request.url)
#            return "There was a problem adding new stuff."
    else:
        # GET - render existing pictures
        logger.debug("GET request.url:'{}'".format(request.url))
        car_pictures = PictureWrapper.query.order_by(PictureWrapper.created_at).all()
        # TODO: When small_pictures_list will be kept in DB, the below code should be cleaned
        # extract small_pictures from db and convert it to list as following:
        # a=car_picture.small_pictures.strip('[]') 
        # pictures_list=a.split()
        for car_picture in car_pictures:
#            car_picture.large_picture = os.path.join(app.config['UPLOAD_FOLDER'], car_picture.name + ".jpg")
#            for small_picture in glob.glob('static/pictures_photo/' + name + '*'):
            logger.debug("car_picture.name: {} car_picture.picture_path from DB: {}".format(car_picture.name, car_picture.picture_path))
            pictures_list = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], car_picture.name + "*"))
            for picture_path in pictures_list:
                small_picture_name = os.path.basename(picture_path)
                small_picture_name = os.path.splitext(small_picture_name)[0]
                if small_picture_name == car_picture.name:
                    car_picture.picture_path = picture_path
                    pictures_list.remove(picture_path)
            car_picture.small_pictures = pictures_list
            logger.debug("car_picture.picture_path: {}".format(car_picture.picture_path))
            logger.debug("car_picture.small_pictures: {}".format(car_picture.small_pictures))
        return render_template('index.html', car_pictures=car_pictures)


@app.route('/delete/<int:id>')
def delete(id):
    car_picture = PictureWrapper.query.get_or_404(id)
    try:
        logger.debug("Delete id:'{}'".format(id))
        db.session.delete(car_picture)
        db.session.commit()
        return redirect('/')
    except:
        logger.error("Update There was a problem deleting data id:'{}'".format(id))
        return "There was a problem deleting data."


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    car_picture = PictureWrapper.query.get_or_404(id)

    if request.method == 'POST':
        logger.debug("POST Update id:'{}'".format(id))
        car_picture.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            logger.error("Update There was a problem updating data id:'{}'".format(id))
            return "There was a problem updating data."

    else:
        logger.debug("GET Update id:'{}'".format(id))
        title = "Update Data"
        return render_template('update.html', title=title, car_picture=car_picture)


if __name__ == '__main__':
    app.run(debug=True)
