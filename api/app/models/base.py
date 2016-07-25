from peewee import *
from datetime import datetime
import config

# Connect to the MySQL database, either production or development, depending on the configuration
db = MySQLDatabase(config.DATABASE['database'], 
    user=config.DATABASE['user'], 
    charset=config.DATABASE['charset'],
    host=config.DATABASE['host'], 
    port=config.DATABASE['port'], 
    passwd=config.DATABASE['password']
)

class BaseModel(Model):
    id = PrimaryKeyField(unique = True)
    created_at = DateTimeField(default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), formats="%Y/%m/%d %H:%M:%S")
    updated_at = DateTimeField(default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), formats="%Y/%m/%d %H:%M:%S")
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return super(BaseModel, self).save(*args, **kwargs)

    def to_hash(self, values):
        values['id'] = self.id
        try:
            values['created_at'] = self.created_at.strftime("%Y/%m/%d %H:%M:%S")
        except:
            values['created_at'] = self.created_at
        try:
            values['updated_at'] = self.updated_at.strftime("%Y/%m/%d %H:%M:%S")
        except:
            values['updated_at'] = self.updated_at
        return values

    class Meta:
        database = db
        order_by = ("id", )
