from db import db

class ItemTages(db.Model):
    __tablename__="items_tags"

    id=db.Column(db.Integer,primary_key=True)
    item_id=db.Column(db.Integer,db.ForeignKey("items.id"))
    tag_id=db.Column(db.Integer,db.ForeignKey("tags.id"))

#many to many relation ship
#secoundary table
