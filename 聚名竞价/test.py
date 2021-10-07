import hashlib
m = hashlib.md5()
m.update(b'[jiami11111mima]')
print(m.hexdigest())

m1 = hashlib.md5()
print(m.hexdigest()[0:19].encode())
m1.update(m.hexdigest()[0:19].encode())
print(m1.hexdigest())
print(m1.hexdigest()[0:19])

# eab1b3c695c7d7f26d7
# eab1b3c695c7d7f26d7