import serial
import serialp.conversions

PROTOCOL_ST = 0x55
PROTOCOL_END = 0x77

class Serial:
    """A class to implement a simple serial protocol.

    The protocol consists in sending the data in the following format:

    - Start - 1 byte
    - Command (or ID) - 4 bytes
    - Number of bytes that will be sent - 4 bytes
    - Data - N bytes
    - End - 1 bytes

    Parameters
    ----------
    com : str
        COM port.

    baud : int
        Baudrate used for communication. By default, it is 9600 bps.

    timeout : int, float
        Communication time-out, in seconds. By default, it is 0.2 s.
    
    """
    def __init__(self, com, baud=9600, timeout=0.2):
        
        self.serial = serial.Serial(com, baud, timeout=timeout)

    
    def send(self, command, data=None):
        """Sends a command and data (optional) through the serial protocol.

        Parameters
        ----------
        command : int
            Command to send.

        data : list or :class:`NoneType`
            Data, as a list of bytes. If `None`, no data is sent.

        """
        data_packet = self.packet(command, data)
        self.serial.write(data_packet)

    
    def read(self, command):
        """Reads an incoming packet.

        Parameters
        ----------
        command : int
            The expected command.

        Returns
        -------
        data : list
            The received data. If any error occurs during transmission (wrong
            command, data-timed out, etc), an empty list is returned.

        """
        # Reads start byte
        st = self.serial.read(1)
        if len(st) != 1:
            print('Start byte timed-out')
            return []

        st = st[0]
        if st != PROTOCOL_ST:
            print('Received wrong start byte')
            return []

        # Reads command byte - should be the same as command
        cmd = self.serial.read(4)
        if len(cmd) != 4:
            print('Command timed-out')
            return []

        cmd1 = serialp.conversions.u8_to_u32(cmd, msb=False)
        if cmd1 != command:
            print('Received wrong command')
            print('Received: {:}. Expected: {:}'.format(cmd1, command))
            print('Bytes: {:}'.format(list(cmd)))
            return []

        # Reads the size of the incoming data
        size = self.serial.read(4)
        if len(size) != 4:
            print('Data size timed-out')
            return []
        
        size = serialp.conversions.u8_to_u32(size, msb=False)

        # Reads the data
        data = self.serial.read(size)
        if len(data) != size:
            print('Data receive timed-out')
            return []
        
        # Reads stop byte
        st = self.serial.read(1)
        if len(st) != 1:
            print('Stop byte timed-out')
            return []

        st = st[0]
        if st != PROTOCOL_END:
            print('Received wrong stop byte')
            return []
        
        return data
    
    
    def packet(self, command, data=None):
        """Mounts an outgoing packet, according to the protocol.

        Parameters
        ----------
        command : int
            Command

        data : list or :class:`NoneType`
            Data. Choose `None` if no data is to be sent.

        Returns
        -------
        list
            A list of bytes containing the formatted data.
            
        """
        data_packet = []
        
        command_u8 = serialp.conversions.u32_to_u8(command)
        if data is None:
            size_u8 = serialp.conversions.u32_to_u8(0)
        else:
            size_u8 = serialp.conversions.u32_to_u8(len(data))
        
        data_packet.extend([PROTOCOL_ST])
        data_packet.extend(command_u8)
        data_packet.extend(size_u8)
        if data is not None:
            data_packet.extend(data)
        data_packet.extend([PROTOCOL_END])
        
        return data_packet
