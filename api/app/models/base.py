from peewee import *
from datetime import datetime
import config

# Connect to the MySQL database, either production or development, depending on the configuration
db = MySQLDatabase(
    host=config.DATABASE['host'], 
    port=config.DATABASE['port'], 
    user=config.DATABASE['user'], 
    password=config.DATABASE['password'],
    database=config.DATABASE['database'], 
    charset=config.DATABASE['charset']
)

class BaseModel(Model):
    id = PrimaryKeyField(unique = True)
    created_at = DateTimeField(default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    updated_at = DateTimeField(default=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        database = db
        order_by = ("id", )
