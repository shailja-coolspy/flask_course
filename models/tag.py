from db import db

class TagModel(db.Model):
    __tablename__="tags"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    store_id=db.Column(db.Integer,db.ForeignKey("stores.id"),nullable=False)

    store=db.relationship("StoreModel",back_populates="tags")
    #back_populate create new attribute in of tags in ItemModel
    #it should match tags attribute in ItemModel
    items=db.relationship("ItemModel",back_populates="tags",secondary="items_tags")

    #two tags can have same name if its store_id is different this has to be handled manually as we can not do with sqlalchemy