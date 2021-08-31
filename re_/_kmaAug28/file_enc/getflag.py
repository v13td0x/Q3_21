with open("flag.jpg.encrypt", "rb") as f:
	enc_file = bytearray(f.read())

file = bytearray(b'')

before_neg = bytearray(b'')
for v in enc_file:
	before_neg.append((256-v)&0xff)

for v3 in range(0, len(enc_file) -1, 8):
	v10 = before_neg[v3:v3+8]
	for i in range(8):
		v5 = 0
		for j in range(8):
			v5 += ((v10[j] >> i) & 1) << j
		file.append(v5)
	v3 += 8
with open("flag.jpg", "wb") as f:
	f.write(file)
