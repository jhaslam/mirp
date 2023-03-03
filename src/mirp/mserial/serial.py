from abc import ABC, abstractmethod
from kivy.utils import platform

from .errors import NoResponseError, InvalidResponseError, HardwareError, HardwarePermissionError

if platform == 'android':
    from usb4a import usb
    from usbserial4a import serial4a
else:
    import serial
    import serial.tools.list_ports
    import serial.tools.list_ports_common


class Serial(ABC):
    @abstractmethod
    def device_names(self) -> [str]:
        """Lists the serial devices detected on the system"""

    @abstractmethod
    def ident_device(self, device_name):
        """Reads the given serial device"""


class DesktopSerial(Serial):
    def device_names(self) -> [str]:
        port_list: [serial.tools.list_ports_common.ListPortInfo] = serial.tools.list_ports.comports()
        device_name_list = [port.device for port in port_list]
        return device_name_list

    def ident_device(self, device_name: str) -> str:
        """Ask radio to identify itself"""
        UV5R_MODEL_291_WAKE: bytes = bytes.fromhex('50 BB FF 20 12 07 25')
        ACK: bytes = bytes.fromhex('06')
        REQUEST_IDEN: bytes = bytes.fromhex('02')
        MAX_RESPONSE_LEN: int = 12
        TERMINATOR: int = 221
        TIMEOUT_SECS = 3

        serial_port = None
        try:
            serial_port = serial.Serial(device_name,
                                        9600,
                                        serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE,
                                        timeout=TIMEOUT_SECS)

            # Wake Device
            serial_port.write(UV5R_MODEL_291_WAKE)
            ack: bytes = serial_port.read(1)
            if not ack:
                raise NoResponseError
            if ack != ACK:
                raise InvalidResponseError

            # Request identifier
            serial_port.write(REQUEST_IDEN)
            ident: bytes = serial_port.read(MAX_RESPONSE_LEN)
            if not ident:
                raise NoResponseError
            if ident[-1] != TERMINATOR:
                raise InvalidResponseError

        except serial.serialutil.SerialException as exc:
            raise HardwareError from exc

        finally:
            if serial_port:
                serial_port.close()

        return ident.hex(" ")


class AndroidSerial(Serial):
    def device_names(self) -> [str]:
        usb_device_list = usb.get_usb_device_list()
        device_name_list = [device.getDeviceName() for device in usb_device_list]
        return device_name_list

    def ident_device(self, device_name: str) -> str:
        """Ask radio to identify itself"""
        UV5R_MODEL_291_WAKE: bytes = bytes.fromhex('50 BB FF 20 12 07 25')
        ACK: bytes = bytes.fromhex('06')
        REQUEST_IDEN: bytes = bytes.fromhex('02')
        MAX_RESPONSE_LEN: int = 12
        TERMINATOR: int = 221
        TIMEOUT_SECS = 3

        serial_device = usb.get_usb_device(device_name)
        if not serial_device:
            raise HardwareError
        if not usb.has_usb_permission(serial_device):
            raise HardwarePermissionError

        serial_port = None
        try:
            serial_port = serial4a.get_serial_port(
                device_name,
                9600,
                8,
                'N',
                1,
                timeout=1
            )

            # Wake Device
            serial_port.write(UV5R_MODEL_291_WAKE)
            ack: bytes = serial_port.read(1)
            if not ack:
                raise NoResponseError
            if ack != ACK:
                raise InvalidResponseError

            # Request identifier
            serial_port.write(REQUEST_IDEN)
            ident: bytes = serial_port.read(MAX_RESPONSE_LEN)
            if not ident:
                raise NoResponseError
            if ident[-1] != TERMINATOR:
                raise InvalidResponseError

        finally:
            if serial_port:
                serial_port.close()

        return ident.hex(" ")

