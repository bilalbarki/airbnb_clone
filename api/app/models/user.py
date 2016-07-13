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
        self.password = m.digest
