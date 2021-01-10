# Create DB
>>> from app import db
>>> db.create_all()
>>> from app import Grocery
>>> obj = Grocery(name='milk')
>>> db.session.add(obj)
>>> db.session.commit()
>>> Grocery.query.all()
[<Grocery 'milk'>]

from components.config import db
from components.lpr_eng import PictureWrapper
db.create_all()
obj = PictureWrapper(name = 'rear_view_lp', picture_path = '')
new_picture = PictureWrapper(name = 'rear_view_lp', picture_path = '', recognized_txt = '', small_pictures = [])
db.session.add(obj)
db.session.commit()
PictureWrapper.query.all()

        <td> <img src="{{url_for('static',filename = 'pictures_photo/rear_view_lp.jpg')}}" class="large_picture" alt="test image" > </td>
        <td> <img src="{{url_for(test_image)}}" class="large_picture" alt="test image" > </td>
        <td> <img src="{{ test_image }}" class="large_picture" alt="test image" > </td>
'C:\Program Files\Tesseract-OCR\tesseract.exe' --psm 13 images/rear_view_lp.jpg ttt
