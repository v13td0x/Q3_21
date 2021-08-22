# SVATTT 2017 :: re100
# 
cmp_data = [0xBF, 0x86, 0x0E2, 0x90, 0x47, 0x42, 0x0C3, 0x0E7, 0x95, 0x0A0, 0x91, 0x41, 0x5, 0x80, 0x0E4, 0x0A0, 0x0A2, 0x0D3, 0x47, 0x45, 0x84, 0x0BF, 0x0B1, 0x0FD, 0x0CD, 0x7, 0x18, 0x0C6, 0x67, 0x33]

def conNonLam():
	v23 = bytearray(30)
	v18 = cmp_data[26]
	v23[26] = 0x34^ cmp_data[25]
	v17 = cmp_data[23]
	v23[23] = cmp_data[27] ^ 0xf2
	v23[25] = cmp_data[24] ^ 0xA1

	v23[27] = v18 ^ 0x76

	v23[24] = v17 ^ 0x91

	v16 = cmp_data[21]
	v23[21] = cmp_data[22] ^ 0xf2

	v23[22] = v16 ^ 0xd7

	v14 = cmp_data[20]
	v23[20] = cmp_data[19] ^ 0x76
	v23[19] = cmp_data[18] ^ 0x34
	v15 = cmp_data[16]
	v23[18] = cmp_data[17] ^ 0xa1

	v23[17] = v15 ^ 0x91

	v13 = cmp_data[14]
	v23[14] = cmp_data[15] ^ 0xf2
	v23[16] = v14 ^ 0xf2

	v23[15] = v13 ^ 0xd7

	v11 = cmp_data[13]
	v23[13] = cmp_data[12] ^ 0x76
	v23[12] = cmp_data[11] ^ 0x34
	v12 = cmp_data[9]
	v23[11] = cmp_data[10] ^ 0xa1

	v23[10] = v12 ^ 0x91

	v10 = cmp_data[7]
	v23[7] = cmp_data[8] ^ 0xf2
	v23[9] = v11 ^ 0xf2

	v23[8] = v10 ^ 0xd7

	v8 = cmp_data[6]
	v23[6] = cmp_data[5] ^ 0x76
	v23[5] = cmp_data[4] ^ 0x34
	v9 = cmp_data[2]
	v23[4] = cmp_data[3] ^ 0xa1

	v23[3] = v9 ^ 0x91

	v7 = cmp_data[0]
	v23[0] = cmp_data[1] ^ 0xf2
	v23[2] = v8 ^ 0xf2

	v23[1] = v7 ^ 0xd7
	# last 2 chars
	v23[28], v23[29] = cmp_data[28], cmp_data[29]
	return v23
print(conNonLam())