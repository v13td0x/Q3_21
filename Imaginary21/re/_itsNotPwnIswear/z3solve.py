from z3 import *

cmp_data = [0x317EE37C444051C9, 0x65BBFA1E87AA1F8D]

inp = [BitVec("%d" % i, 64) for i in range(2)]
s = Solver()
s.add((0x6231726435333364 * inp[0] + inp[1]) & 0xffffffffffffffff == cmp_data[0])
s.add((cmp_data[0] * inp[0] + inp[1]) & 0xffffffffffffffff == cmp_data[1])

if s.check() == sat:
    ans = bytearray(b'')
    m = s.model()
    md = sorted([(d, m[d]) for d in m], key = lambda x: str(x[0]))
    for i in md:
        int64_i = i[1].as_long()
        ans.extend(int64_i.to_bytes((int64_i.bit_length()+7)//8, 'little'))
print(b'A'*10 + ans)