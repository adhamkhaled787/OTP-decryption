from collections import defaultdict

with open("ciphers.txt") as f:
    hex_lines = [line.strip() for line in f]
print(f" hex_lines:{hex_lines[0]}")

ciphers = [bytes.fromhex(h) for h in hex_lines]

print(f"ciphers :{ciphers[0]}")


def xor_bytes(b1, b2):
    length = min(len(b1), len(b2))
    return [b1[i] ^ b2[i] for i in range(length)]

def is_letter(a):
    if (65<= a <= 90) or (97<= a <=122):
        return True
    else:
        return False
    
n = len(ciphers)
space_votes = defaultdict(int)

for i in range(n):
    for j in range(n):
        if i==j: 
            continue
        maxpos = min(len(ciphers[i]),len(ciphers[j]))
        for pos in range(maxpos):
            x = ciphers[i][pos] ^ ciphers[j][pos]
            if is_letter(x):
                space_votes[(i, pos)] += 1

threshold = 4

likely_space  = set()

for (i,pos), votes in space_votes.items():
    if votes >= threshold:
        likely_space.add((i,pos))





