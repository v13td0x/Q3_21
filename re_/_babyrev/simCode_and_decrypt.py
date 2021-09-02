inp = b'aamPL47e1nputTe5tvwxyzABCDEFGHIJ'
cmp_data = [0xA4, 0x0AD, 0x0C0, 0x0A3, 0x0FD, 0x7F, 0x0AB, 0x0, 0x0E8, 0x0D5, 0x0E2, 0x48, 0x0DA, 0x0BF, 0x0FD, 0x0, 0x0D1, 0x40, 0x0F2, 0x0C4, 0x7B, 0x0BF, 0x76, 0x0, 0x87, 0x7, 0x0D5, 0x0AD, 0x0AE, 0x82, 0x0FD, 0x0]
def check(in_):
	v4 = bytearray(b'')
	if(len(in_) != 32):
		return 1
	for i in range(0, len(in_)-1, 8):
		v5 = in_[i:i+8]
		v4.extend(bytearray(calc_qword(v5)))
	return v4

def calc_qword(qword):
	src = [0]*8
	for i in range(8):
		v3 = qword[i]
		for j in range(8):
			src[j] = src[j]|(v3&1) << i
			v3 >>= 1
	return src
print(check(inp))
print(check(cmp_data))