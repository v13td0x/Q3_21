content = b'viet_dox_hahodiashfask00_ahiahkhakljuioh'
output = bytearray(b'')

v3 = 0
while(v3 < len(content)):
	v10 = content[v3:v3+8]
	Src = [0]*8
	for i in range(8):
		v5 = 0
		for j in range(8):
			v5 += ((v10[j] >> i) & 1) << j
		Src[i] = (256 - v5)& 0xff
	for x in Src:
		output.append(x)
	v3 += 8
print(output)
