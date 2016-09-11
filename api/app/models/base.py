from peewee import *
from datetime import datetime
import config

# Defines MySQLDatabase details, either production, development or test, depending on the configuration
db = MySQLDatabase(
    host=config.DATABASE['host'], 
    port=config.DATABASE['port'], 
    user=config.DATABASE['user'], 
    password=config.DATABASE['password'],
    database=config.DATABASE['database'], 
    charset=config.DATABASE['charset']
)

'''base model used as a base for most other tables'''
class BaseModel(Model):
    id = PrimaryKeyField(unique = True)
    created_at = DateTimeField(default=datetime.now(), formats="%Y/%m/%d %H:%M:%S")
    updated_at = DateTimeField(default=datetime.now(), formats="%Y/%m/%d %H:%M:%S")
    
    '''override of save method, runs just before saving data to database'''
    def save(self, *args, **kwargs):
        if self._get_pk_value() is None:
            # this is a create operation
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

    '''returns base model data as a dict'''
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.strftime("%Y/%m/%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y/%m/%d %H:%M:%S")
        }

    class Meta:
        database = db
        order_by = ("id", )
