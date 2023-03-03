import sys

# These are the same
# UV5R_MODEL_291: bytes = b'\x50\xBB\xFF\x20\x12\x07\x25'
UV5R_MODEL_291: bytes = bytes.fromhex('50 BB FF 20 12 07 25')

print(UV5R_MODEL_291)
print(type(UV5R_MODEL_291))
print(f'Length of bytes: {len(UV5R_MODEL_291)}')
print()

byte_array = bytearray(UV5R_MODEL_291)
print(f'byte array: {byte_array.hex(" ")}')
for byte in byte_array:
    print(f'byte in bytearray: {byte}')


print(f'iterating through: {UV5R_MODEL_291.hex(" ")}')
for int_byte in UV5R_MODEL_291:
    byte_byte: bytes = int_byte.to_bytes(1, sys.byteorder)
    print(f'current byte: {byte_byte.hex(" ")}')
    str_byte: str = str(byte_byte)
    byte_byte


wholestring_bytes = UV5R_MODEL_291.hex(' ')
print(f'all bytes = {wholestring_bytes}')





#bytes(received_msg).decode('utf8')

