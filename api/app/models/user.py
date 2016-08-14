import base
from hashlib import md5
from peewee import *

class User(base.BaseModel):
    email = CharField(null=False, unique=True, max_length=128)
    password = CharField(null=False, max_length=128)
    first_name = CharField(null=False, max_length=128)
    last_name = CharField(null=False, max_length=128)
    is_admin = BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._get_pk_value() is None:
            self.password = self.set_password(self.password) # at row creation, convert password to md5 before saving
        return super(User, self).save(*args, **kwargs)

    def set_password(self, clear_password):
        m = md5()
        m.update(clear_password)
        return m.hexdigest()

    def to_dict(self):
        user_dict = super(User, self).to_dict()

        user_dict.update({
            "first_name": self.first_name,
            "email": self.email,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
        })
        return user_dict
        

