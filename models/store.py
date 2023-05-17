from db import db

class StoreModel(db.Model):
    __tablename__="stores"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(90),unique=True,nullable=False)
    #lazy means items from the database will not be pre fetched ,it will be fetched when we ask it to,it speed up database
    #cascade means when we delete a store its item will also be deleted
    #Store is parent
    item=db.relationship("ItemModel",back_populates="store",lazy="dynamic",cascade="all,delete")
    tags=db.relationship("TagModel",back_populates="store",lazy="dynamic")