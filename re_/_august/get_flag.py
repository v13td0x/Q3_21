def inverse_Fp(a, p):
	u = a
	v = p
	x1, x2 = 1, 0
	while(u != 1):
		q = v // u
		r = v - q*u
		x = x2-q*x1

		v = u
		u = r
		x2 = x1
		x1 = x
	return x1%p



# 7, 3
p = b'ITISNICETODAY'
for pi in p:
	print(chr(((7 * (pi - ord('A')) +3) % 26) + ord('A')), end = '')
C = b'HGHZQHRFGXYDP'
print()
for ci in C:
	print(chr(((15 * ((ci - ord('A')) -3) % 26)) + ord('A')), end = '')
print()