from z3 import *
# babyrev zh3r0 CTF
cmp_data = [0xA4, 0x0AD, 0x0C0, 0x0A3, 0x0FD, 0x7F, 0x0AB, 0x0, 0x0E8, 0x0D5, 0x0E2, 0x48, 0x0DA, 0x0BF, 0x0FD, 0x0, 0x0D1, 0x40, 0x0F2, 0x0C4, 0x7B, 0x0BF, 0x76, 0x0, 0x87, 0x7, 0x0D5, 0x0AD, 0x0AE, 0x82, 0x0FD, 0x0]
inp = bytearray(b'')

for i_len_enc in range(0, 32, 8):
    src = [0]*8

    qword = [BitVec("%d" %i, 8) for i in range(8)]
    s = Solver()

    for i in range(8):
        v3 = qword[i]
        for j in range(8):
            src[j] = src[j]|(v3&1) << i
            v3 >>= 1
    s.add(src[0] == cmp_data[0+i_len_enc])
    s.add(src[1] == cmp_data[1+i_len_enc])
    s.add(src[2] == cmp_data[2+i_len_enc])
    s.add(src[3] == cmp_data[3+i_len_enc])
    s.add(src[4] == cmp_data[4+i_len_enc])
    s.add(src[5] == cmp_data[5+i_len_enc])
    s.add(src[6] == cmp_data[6+i_len_enc])
    s.add(src[7] == cmp_data[7+i_len_enc])
    if s.check() == sat:
        ans = bytearray(b'')
        m = s.model()
        md = sorted([(d, m[d]) for d in m], key = lambda x: str(x[0]))
        for i in md:
            ans.append(i[1].as_long())
        inp.extend(ans)
print(inp)