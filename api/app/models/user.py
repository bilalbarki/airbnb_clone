import base
from hashlib import md5
from peewee import *

'''Defines User'''
class User(base.BaseModel):
    email = CharField(null=False, unique=True, max_length=128)
    password = CharField(null=False, max_length=128)
    first_name = CharField(null=False, max_length=128)
    last_name = CharField(null=False, max_length=128)
    is_admin = BooleanField(default=False)

    '''converts password to md5 before saving it in database'''
    def save(self, *args, **kwargs):
        if self._get_pk_value() is None:
            self.password = self.set_password(self.password) # at row creation, convert password to md5 before saving
        return super(User, self).save(*args, **kwargs)

    '''coverts clear password to md5'''
    def set_password(self, clear_password):
        m = md5()
        m.update(clear_password)
        return m.hexdigest()

    '''returns row of user in a dict'''
    def to_dict(self):
        user_dict = super(User, self).to_dict()

        user_dict.update({
            "first_name": self.first_name,
            "email": self.email,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
        })
        return user_dict
        

