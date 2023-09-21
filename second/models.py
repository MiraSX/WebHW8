from connect import connect
from mongoengine import Document
from mongoengine.fields import BooleanField, StringField


class Contacts(Document):
    fullname = StringField()
    email = StringField()
    address = StringField()
    sent = BooleanField(default=False)
