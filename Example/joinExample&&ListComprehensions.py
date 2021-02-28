import pwn

# Example of pwn generating a buffer
# a = ''.join(chr(i) for i in range(ord('0'), ord('z')))
print(bytes(pwn.cyclic(length=2000, alphabet=''.join(chr(i) for i in range(ord('0'), ord('z')))), encoding='UTF-8'))

# Example of the join & list Comprehension
exclude = (0x0, 0xa, 0xd, 0xff)
payload = b''.join(bytes([i]) for i in range(1, 256) if i not in exclude)
print(payload)
