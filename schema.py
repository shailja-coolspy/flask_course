from marshmallow import Schema,fields

#"Marshmallow" can only checks incoming data.
#The Json that client sends is passed through the ItemSchema,it checks that the fields are there and they are of valid type.
# Then,it give method an argument,which is that validated dictionary...
#"Marshmallow" can turn object into json

#ItemSchema has nested LIST OF store
#StoreSchema has nested LIST OF item

#PlainItemSchema does not know about store and does not deal with it
class PlainItemSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)
    price=fields.Float(required=True)

#PlainStoreSchema does not know about item and does not deals with it
class PlainStoreSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)

class PlainTagSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)
class ItemUpdateSchema(Schema):
    name=fields.Str()
    price=fields.Float()
    store_id=fields.Int()

#We use PlainStoreSchema or PlainItemSchema to avoid recursive nesting::::
#ItemSchema will inherit from PlainItemSchema
class ItemSchema(PlainItemSchema):
    store_id=fields.Int(required=True,load_only=True)
    #will use store when returning data to client not while receiving data
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagSchema()),dump_only=True)



class StoreSchema(PlainStoreSchema):
    items=fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagSchema()),dump_only=True)

class TagSchema(PlainTagSchema):
    store_id=fields.Int(required=True,load_only=True)
    #will use store when returning data to client not while receiving data
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    items=fields.List(fields.Nested(PlainItemSchema()),dump_only=True)

class TagAndItemSchema(Schema):
    message=fields.Str()
    item=fields.Nested(ItemSchema)
    tag=fields.Nested(TagSchema)


class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    username=fields.Str(required=True)
    #"load_only" as password should not we saved in file
    #api cannot sent back password to client only user can send it to api
    password=fields.Str(required=True,load_only=True)


