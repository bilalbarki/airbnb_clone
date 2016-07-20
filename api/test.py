from hashlib import md5

m = md5()
m.update("bilal")
print m.hexdigest()
