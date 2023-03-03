class MSerialError(Exception):
    pass


class InvalidResponseError(MSerialError):
    pass


class NoResponseError(InvalidResponseError):
    pass


class HardwareError(MSerialError):
    pass


class HardwarePermissionError(HardwareError):
    pass