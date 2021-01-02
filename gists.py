# Create DB
>>> from app import db
>>> db.create_all()
>>> from app import Grocery
>>> obj = Grocery(name='milk')
>>> db.session.add(obj)
>>> db.session.commit()
>>> Grocery.query.all()
[<Grocery 'milk'>]

from app import db
db.create_all()
from app import Pictures
obj = Pictures(name='milk')
db.session.add(obj)
db.session.commit()
Pictures.query.all()

        <td> <img src="{{url_for('static',filename = 'pictures_photo/rear_view_lp.jpg')}}" class="large_picture" alt="test image" > </td>
        <td> <img src="{{url_for(test_image)}}" class="large_picture" alt="test image" > </td>
        <td> <img src="{{ test_image }}" class="large_picture" alt="test image" > </td>
