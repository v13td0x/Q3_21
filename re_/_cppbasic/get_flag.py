cmp_enc = "af656565652f4f864e6ceb8eaa4ceb65656cebac8d0ead266e6f686a6869"
flag = ''
for i in range(0, len(cmp_enc), 2):
	h = int(cmp_enc[i]+ cmp_enc[i+1], 16)
	for ch in range(0x30, 0x7e):
		if(h == ((ch >> 3) | (ch << 5)) & 0xff):
			flag += chr(ch)
print(flag[::-1])