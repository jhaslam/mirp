from src.mirp.mserial.errors import NoResponseError, InvalidResponseError

IDEN_RAW: bytes = bytes.fromhex('aa 36 74 04 00 05 20 dd')
IDEN: bytes = bytes.fromhex('36 74 04 00 05 20')
ID: bytes = bytes.fromhex('50 20 12 07 25')
TERMINATOR: int = 221


# decoded_iden: str = ''
# try:
#     decoded_iden = IDEN_RAW.decode()
# except UnicodeDecodeError:
#     decoded_iden = IDEN_RAW.hex(" ")
#
# print(decoded_iden)

iden = IDEN_RAW

if not iden:
    raise NoResponseError
if iden[-1] != TERMINATOR:
    raise InvalidResponseError