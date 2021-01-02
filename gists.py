# Create DB
>>> from app import db
>>> db.create_all()
>>> from app import Grocery
>>> obj = Grocery(name='milk')
>>> db.session.add(obj)
>>> db.session.commit()
>>> Grocery.query.all()
[<Grocery 'milk'>]