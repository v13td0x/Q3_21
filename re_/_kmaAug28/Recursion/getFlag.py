param_data = [0x7, 0x9, 0x13, 0x5, 0x106, 0xB6, 0x21, 0x70, 0x86, 0x0C, 0x88, 0x37, 0x135, 0x21, 0x0EF, 0x54, 0x195, 0x37, 0x79, 0x54, 0x0D7, 0x21, 0x86, 0x0C, 0x0EF, 0x21, 0x17, 0x0EF, 0x17, 0x17B, 0x135, 0x25, 0x29]
# max = 405
# simulation code
def rec(n):
	if(n == 0):
		return 0
	elif(n == 1):
		return 1
	elif(n == 2):
		return 2
	return 17 * rec(n - 3) + 3 * rec(n-2) + 75 * rec(n-1)

# solve
recA = [0, 1, 2]
n = 3
while(n < 406):
	recA.append((17 * recA[n - 3] + 3 * recA[n-2] + 75 * recA[n-1])&0xff)
	n += 1
for i in param_data:
	print(chr(recA[i]), end = '')