from z3 import *

with open("flag.jpg.encrypt", "rb") as f:
	enc = f.read()

data = [0 for i in range(len(enc))]

for i_len_enc in range(0, len(enc) - 1, 8):

	inp = [BitVec("%d" % i, 8) for i in range(8)]
	s = Solver()
	rs = 0

	for i in range(0, 8):
		rs = 0
		for j in range(0, 8):
			rs += ((inp[j] >> i) & 1) << j
		rs = 0xFF - (rs & 0xFF) + 1

		s.add(rs == enc[i_len_enc + i])

	if s.check() == sat:
		flag = []
		m = s.model()
		md = sorted([(d, m[d]) for d in m], key = lambda x: str(x[0]))
		for i in md:
			flag.append(i[1].as_long())
		
		for i in range(0, 8):
			data[i_len_enc + i] = flag[i]

with open("flag.jpg", "wb") as f:
	f.write(bytearray(data))

print("Done!")