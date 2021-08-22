# RE3 Catalyst system AlexCTF 2017

# for a1 in range(50):
# 	if (4 * (a1 >> 2) != a1 or 4 * (a1 >> 4) == a1 >> 2 or (a1 >> 3) == 0 or a1 >> 4 ):
# 		continue
# 	print(a1)
'''
len(username) = 8 or 12
'''

'''
sat
[c = 1868915551, b = 1953724780, a = 1635017059]

'''
a = 1635017059
b = 1953724780
c = 1868915551
print(a.to_bytes(4, 'little') + b.to_bytes(4, 'little') + c.to_bytes(4, 'little'))

rand = [0x684749, 0x673ce537, 0x7b4505e7, 0x70a0b262, 0x33d5253c, 0x515a7675, 0x596d7d5d, 0x7cd29049, 0x59e72db6, 0x4654600d]
cmp_val = [0x55EB052A, 0xEF76C39, 0xCC1E2D64, 0xC7B6C6F5, 0x26941BFA, 0x260CF0F3, 0x10D4CAEF, 0xC666E824, 0xFC89459C, 0x2413073A]
passw = b''
for i in range(10):
	v = cmp_val[i] + rand[i]
	passw += v.to_bytes(5, 'little')[:4]
print(passw)