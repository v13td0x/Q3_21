cmp_data = b'OMsra n ne defotsnM'
len_ = len(cmp_data)

input = bytearray(len_)
for i in range(len_):
	input[3*i % len_] = cmp_data[i]
print(input)