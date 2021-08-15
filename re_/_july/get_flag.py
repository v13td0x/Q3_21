int64_lst =  [0xC0FEC0FE0879D8F2, 0xC0FEC0FE038E4585, 0xC0FEC0FE00E47451, 0xC0FEC0FE03ACED01,
 0xC0FEC0FE0222FC22, 0xC0FEC0FE03BC9092, 0xC0FEC0FE03F92160, 0xC0FEC0FE03919685,
 0xC0FEC0FE0DCEE9EA, 0xC0FEC0FE0390EB29, 0xC0FEC0FE0B338C70, 0xC0FEC0FE03903806,
 0xC0FEC0FE0879E4E5, 0xC0FEC0FE03BCCEC4, 0xC0FEC0FE04EB5981, 0xC0FEC0FE01C83D3C,
 0xC0FEC0FE04BE55A5, 0xC0FEC0FE03ADD2A4, 0xC0FEC0FE05A15051, 0xC0FEC0FE019BFFDF,
 0xC0FEC0FE09A8F7FD, 0xC0FEC0FE02ACBD14, 0xC0FEC0FE08982740, 0xC0FEC0FE03717D0C,
 0xC0FEC0FE06EF7387, 0xC0FEC0FE0361F4BE, 0xC0FEC0FE05837B7B, 0xC0FEC0FE0391D8B2,
 0xC0FEC0FE0ED0A2A0, 0xC0FEC0FE031576FB, 0xC0FEC0FE02F70EA0, 0xC0FEC0FE02AE61A7,
 0xC0FEC0FE0EFE176E, 0xC0FEC0FE02E7BFDC, 0xC0FEC0FE02227F51, 0xC0FEC0FE01D6767C,
 0xC0FEC0FE01116D3A, 0xC0FEC0FE019CB310, 0xC0FEC0FE0C62D573, 0xC0FEC0FE0352226B,
 0xC0FEC0FE02F73C66, 0xC0FEC0FE0360A5AE, 0xC0FEC0FE006A91E0, 0xC0FEC0FE018D03BC,
 0xC0FEC0FE0A5EE2BA, 0xC0FEC0FE025179CE, 0xC0FEC0FE079661E8, 0xC0FEC0FE03BBBE37,
 0xC0FEC0FE00C5E41F, 0xC0FEC0FE02C91881, 0xC0FEC0FE00E47894, 0xC0FEC0FE03BD85DE,
 0xC0FEC0FE07B4726C, 0xC0FEC0FE02AE521F, 0xC0FEC0FE0EC19AA2, 0xC0FEC0FE039D35B5,
 0, 0, 0, 0]
flag_chars = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_{}"
def gen_int64(buff):
	v3 = 0
	for i in range(3):
		v3 = (997 * v3 + buff[i]) % 0x3B9ACA03;
	return 2 * (v3 | 0xC0FEC0FE00000000) - (~v3 & 0xC0FEC0FE00000000) - (v3 & 0x3F013F01FFFFFFFF)

def checkNewByte(barr_, b_, val):
	barr_.append(b_)
	if(gen_int64(barr_) == val):
		return True
	return False

def brute():
	goal = bytearray(b'\x8f\x3c\x0f') # 3 ki tu dau co dc do brute
	i = 1
	while(int64_lst[i]):
		for b in range(0xff):
			if(checkNewByte(goal[i:], b, int64_lst[i])):
				goal.append(b)
				break
		i += 1
	return goal

def find_v76(b_e, b1_e):
	for v7 in flag_chars:
		for v6 in flag_chars:
			b = 0
			b1 = 0
			for j in range(4):
				b = (2 * (((v7 >> (7 - j)) | 1) - (((v7 >> (7 - j)) & 1) == 0) - ((v7 >> (7 - j)) & 0xFE))) | (4 * b) | (((v6 >> (7 - j)) | 1) - (((v6 >> (7 - j)) & 1) == 0) - ((v6 >> (7 - j)) & 0xFE))
				b1 = (2 * (((v7 >> (3 - j)) | 1) - (((v7 >> (3 - j)) & 1) == 0) - ((v7 >> (3 - j)) & 0xFE))) | (4 * b1) | (((v6 >> (3 - j)) | 1) - (((v6 >> (3 - j)) & 1) == 0) - ((v6 >> (3 - j)) & 0xFE))
			if(b == b_e and b1 == b1_e):
				return v7, v6
	return 0, 0

flag = ''
# print(brute())
input_before_check = bytearray(b"\x8f<\x0f>$?C<\xe9<\xbd<\x8f?S\x1eP>_\x1b\xa3-\x91:u9]<\xfa42-\xfd1$\x1f\x12\x1b\xd1829\x07\x1a\xaf\'\x80?\r/\x0f?\x82-\xf9=\x00\x00")
for i in range(0, len(input_before_check), 2):
	input_before_check[i], input_before_check[i+1] = input_before_check[i+1], input_before_check[i]

for i in range(0, len(input_before_check), 2):
	v7, v6 = find_v76(input_before_check[i], input_before_check[i+1])
	flag += chr(v7) + chr(v6)
print(flag)