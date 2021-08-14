hFile = open("flag.txt.enc", "rb")
enc_flag = bytearray(hFile.read())
key = [0xDEADBEEF, 0xBAADF00D, 0xFEEDFACE, 0xCAFEBABE, 0xDEADBABE, 0xD15EA5E, 0xDECEA5ED, 0xBAADAC1D]
# little endian with dword
for i in range(0, len(enc_flag), 4):
	enc_flag[i], enc_flag[i+1], enc_flag[i+2], enc_flag[i+3] = enc_flag[i+3], enc_flag[i+2], enc_flag[i+1], enc_flag[i]
for i in range(0, len(enc_flag), 8):
	v5 = int(enc_flag[i:i+4].hex(), 16)
	v4 = int(enc_flag[i+4:i+8].hex(), 16)
	for j in range(8):
		v4 = v4 ^ v5 ^ key[8-1-j]
		v5 = v5 ^ v4 ^ key[8-1-j]
	print(v4.to_bytes(4, 'little'))
	print(v5.to_bytes(4, 'little'))