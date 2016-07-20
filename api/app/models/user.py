import base
from hashlib import md5
from peewee import *

class User(base.BaseModel):
    email = CharField(null=False, unique=True, max_length=128)
    password = CharField(null=False, max_length=128)
    first_name = CharField(null=False, max_length=128)
    last_name = CharField(null=False, max_length=128)
    is_admin = BooleanField(default=False)

    def set_password(self, clear_password):
        m = md5()
        m.update(clear_password)
        return m.hexdigest()

    def to_hash(self):
        values = {
            "first_name":self.first_name,
            "email":self.email,
            "last_name":self.last_name,
            "is_admin":self.is_admin 
        }
        return super(User, self).to_hash(values)

