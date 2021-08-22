def char_constrains(v23):
	if ( v23[0] == 0xF2):
		return 0
	v7 = v23[1] ^ 0xD7
	if ( v23[1] == 0xD7):
		return 0
	v8 = v23[2] ^ 0xF2
	v23[1] = v23[0] ^ 0xF2
	v23[0] = v7
	if ( v23[2] == 0xF2):
		return 0
	v9 = v23[3] ^ 0x91
	if ( v23[3] == 0x91):
		return 0
	if ( v23[4] == 0xA1):
		return 0
	if ( v23[5] == 0x34):
		return 0
	if ( v23[6] == 0x76):
		return 0
	v23[3] = v23[4] ^ 0xA1
	v23[2] = v9
	v23[4] = v23[5] ^ 0x34
	v23[5] = v23[6] ^ 0x76
	v23[6] = v8
	if ( v23[7] == 0xF2):
		return 0
	v10 = v23[8] ^ 0xD7
	if ( v23[8] == 0xD7):
		return 0
	v11 = v23[9] ^ 0xF2
	v23[8] = v23[7] ^ 0xF2
	v23[7] = v10
	if ( v23[9] == 0xF2):
		return 0
	v12 = v23[10] ^ 0x91
	if ( v23[10] == 0x91):
		return 0
	if ( v23[11] == 0xA1):
		return 0
	if ( v23[12] == 0x34):
		return 0
	if ( v23[13] == 0x76):
		return 0
	v23[10] = v23[11] ^ 0xA1
	v23[9] = v12
	v23[11] = v23[12] ^ 0x34
	v23[12] = v23[13] ^ 0x76
	v23[13] = v11
	if ( v23[14] == 0xF2):
		return 0
	v13 = v23[15] ^ 0xD7
	if ( v23[15] == 0xD7):
		return 0
	v14 = v23[16] ^ 0xF2
	v23[15] = v23[14] ^ 0xF2
	v23[14] = v13
	if ( v23[16] == 0xF2):
		return 0
	v15 = v23[17] ^ 0x91
	if ( v23[17] == 0x91):
		return 0
	if ( v23[18] == 0xA1):
		return 0
	if ( v23[19] == 0x34):
		return 0
	if ( v23[20] == 0x76):
		return 0
	v23[17] = v23[18] ^ 0xA1
	v23[16] = v15
	v23[18] = v23[19] ^ 0x34
	v23[19] = v23[20] ^ 0x76
	v23[20] = v14
	if ( v23[21] == 0xF2):
		return 0
	v16 = v23[22] ^ 0xD7
	if ( v23[22] == 0xD7):
		return 0
	v23[22] = v23[21] ^ 0xF2
	v23[21] = v16
	if ( v23[23] == 0xF2):
		return 0
	v17 = v23[24] ^ 0x91
	if ( v23[24] == 0x91):
		return 0
	if ( v23[25] == 0xA1):
		return 0
	if ( v23[26] == 0x34):
		return 0
	v18 = v23[27] ^ 0x76
	if ( v23[27] == 0x76):
		return 0
	v23[24] = v23[25] ^ 0xA1
	v23[27] = v23[23] ^ 0xF2
	v23[23] = v17
	v23[25] = v23[26] ^ 0x34
	v23[26] = v18

cmp_data = [0xBF, 0x86, 0x0E2, 0x90, 0x47, 0x42, 0x0C3, 0x0E7, 0x95, 0x0A0, 0x91, 0x41, 0x5, 0x80, 0x0E4, 0x0A0, 0x0A2, 0x0D3, 0x47, 0x45, 0x84, 0x0BF, 0x0B1, 0x0FD, 0x0CD, 0x7, 0x18, 0x0C6, 0x67, 0x33]
