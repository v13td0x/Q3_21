key = [0xDEADBEEF, 0xBAADF00D, 0xFEEDFACE, 0xCAFEBABE, 0xDEADBABE, 0xD15EA5E, 0xDECEA5ED, 0xBAADAC1D]
flag = bytearray(b'kcsc{viet_dox_f4k3_flag_ahihiho}')

def print_enc_flag(hex_dw0, hex_dw1):
	hex_dw0 = hex_dw0[::-1]
	hex_dw1 = hex_dw1[::-1]
	for i in range(0, len(hex_dw0), 2):
		print(hex_dw0[i+1]+hex_dw0[i], end = ' ')
	for j in range(0, len(hex_dw1), 2):
		print(hex_dw1[j+1]+hex_dw1[j], end = ' ')
	print()
# little endian
def get_dword_num(b_ar):
	return b_ar[3] << 24 ^ b_ar[2] << 16 ^ b_ar[1] << 8 ^ b_ar[0]

def enc(flag):
	for i in range(0, len(flag), 8):
		v4 = get_dword_num(flag[i:i+4])
		v5 = get_dword_num(flag[i+4:i+8])
		for j in range(8):
			v5 = v5 ^ v4 ^ key[j]
			v4 = v4 ^ v5 ^ key[j]
		print_enc_flag(hex(v5)[2:], hex(v4)[2:])
enc(flag)