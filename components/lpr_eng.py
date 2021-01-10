# run.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import argparse
import pytesseract

import sys, os
from components import lpr_utils
from components.config import db, app, logger, allowed_file, datetimeformat, PICTURES_FOLDER, ALLOWED_EXTENSIONS, DATE_FORMAT


class PictureWrapper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    picture_path = db.Column(db.String(180), nullable=False)
    recognized_txt = db.Column(db.String(80), nullable=False)
    small_pictures  = db.Column(db.String(1024), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return '<Picture: %r>' % self.name

def invoke_lpr_eng(name, picture_path):
    logger.debug("invoke_lpr_eng for picture_path:'{}'".format(picture_path))
    config = r'--psm 13'
    recognized_txt, small_pictures = lpr_utils.license_plate_recognition(
        img_path = picture_path,
        new_size = None,
#        blurring_method=alpr.bilateral_filter,
#        binarization_method=alpr.adaptive_threshold
#        blurring_method=alpr.gaussian_blur,
#        binarization_method=alpr.adaptive_threshold
        blurring_method = lpr_utils.median_blur,
        binarization_method = lpr_utils.adaptive_threshold,
        config_str = config
    )
    logger.debug("Going to update DB with new picture: '{}', '{}' ".format(name, picture_path))
    new_picture = PictureWrapper(name = name, picture_path = picture_path, recognized_txt = recognized_txt, small_pictures = str(small_pictures))
    db.session.add(new_picture)
    db.session.commit()

    return new_picture


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="Path to the image")
    args = vars(ap.parse_args())

#    recognized_text = alpr.license_plate_recognition(args['image'], None, gaussian_blur, threshold_otsu)
    recognized_text = alpr.license_plate_recognition(
        img_path=args['image'],
        new_size=None,
#        blurring_method=alpr.bilateral_filter,
#        binarization_method=alpr.adaptive_threshold
#        blurring_method=alpr.gaussian_blur,
#        binarization_method=alpr.adaptive_threshold
        blurring_method=alpr.median_blur,
        binarization_method=alpr.adaptive_threshold
    )

    print("Recognized text: {}",(recognized_text))
    print(recognized_text)
