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

key = {}

for(i,pos) in likely_space:
        if pos < len(ciphers[i]):
            key[pos] = ciphers[i][pos] ^ 0x20

print(f"key bytes recovered: {len(key)}")

def is_letter_or_space(b):
    if (b==32) or (65<=b<=90) or (97<=b<=122):
        return True
    else:
        return False

messages = [["_" for _ in range(len(c))] for c in ciphers]

def decrypt():
    for pos, k in key.items():
        for i , c in enumerate(ciphers):
            if pos < len(c):
                ch = c[pos] ^ k
                if is_letter_or_space(ch):
                    messages[i][pos] = chr(ch)

def print_message():
    for i , row in enumerate(messages):
        print(f"Message {i} : {''.join(row)}")

decrypt()
print_message()

guess0 = "_na_le two factor authentication __ all accounts __ i_pr__e security"



def apply_guess_to_key(guess,m):
    if len(guess) != len(ciphers[m]):
        raise ValueError("lenght of guess is incorrect")
    new_positions = []
    for pos, ch in enumerate(guess):
        if ch == "_" :           
            continue
        if not (ch == " " or ('A' <= ch <= 'Z') or ('a' <= ch <= 'z')):
            raise ValueError(f"Invalid character in guess at pos {pos}: {repr(ch)}")
        kbyte = ciphers[m][pos] ^ ord(ch)
        
        valid = True
        for j, c in enumerate(ciphers):
            if pos < len(c):
                pt = c[pos] ^ kbyte
                if not (pt == 32 or (65 <= pt <= 90) or (97 <= pt <= 122)):
                    valid = False
                    break
        if valid:
            if pos not in key:
                key[pos] = kbyte
                new_positions.append(pos)
    return new_positions

# 3) apply the guess, show what changed, then decrypt & print
newpos = apply_guess_to_key(guess0,0)
print(f"Added {len(newpos)} new key positions from guess0: {sorted(newpos)}")
decrypt()
print_message()
guess1 = "_ee_ your software and devices updated to reduce __te_ti__ th____s y"
newpos = apply_guess_to_key(guess1,1)
print(f"Added {len(newpos)} new key positions from guess0: {sorted(newpos)}")
decrypt()
print_message()
guess5 = "review application permissions often and disable __ne_es__ry privacy"
newpos = apply_guess_to_key(guess5,5)
print(f"Added {len(newpos)} new key positions from guess5: {sorted(newpos)}")
decrypt()
print_message()
guess6 = "be mindful of what you share on social media to protect your ____ac "
newpos = apply_guess_to_key(guess6,6)
print(f"Added {len(newpos)} new key positions from guess6: {sorted(newpos)}")
decrypt()
print_message()
plaintexts = [
    "enable two factor authentication on all accounts to improve security",
    "keep your software and devices updated to reduce potential threats",
    "never click on any links from unknown emails or suspicious messages",
    "back up your data regularly to protect against loss or corruption",
    "lock your devices when you are away to prevent unauthorized access",
    "review application permissions often and disable unnecessary ones",
    "be mindful of what you share on social media to protect your privacy",
    "stay informed about new scams and security threats to be prepared"
]

# print all messages clearly
for i, msg in enumerate(plaintexts):
    print(" ")
    print ("Final Messages")
    print(f" Message {i}: {msg}")
