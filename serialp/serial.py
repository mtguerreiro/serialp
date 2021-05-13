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
        
    """
    def __init__(self, com, baud=9600, timeout=0.2):
        
        self.serial = serial.Serial(com, baud, timeout=timeout)

    
    def send(self, command, data):
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
            The received data.

        """
        # Reads start byte
        st = self.serial.read(1)[0]
        if st != PROTOCOL_ST:
            return []

        # Reads command byte - should be the same as command
        cmd = self.serial.read(4)
        if len(cmd) != 4:
            return []
        
        cmd = serialp.conversions.u8_to_u32(cmd, msb=False)
        if cmd != command:
            return []

        # Reads the size of the incoming data
        size = self.serial.read(4)
        if len(size) != 4:
            return []
        
        size = serialp.conversions.u8_to_u32(size, msb=False)

        # Reads the data
        data = self.serial.read(size)
        if len(data) != size:
            return []
        
        # Reads stop byte
        st = self.serial.read(1)[0]
        print(st)
        if st != PROTOCOL_END:
            return []

        #If everything went well, return the data
        
        return data
    
    
    def packet(self, command, data=None):
        """Mounts an outgoing packet, according to the protocol.

        Parameters
        ----------
        command : int
            Command

        data : list or :class:`NoneType`
            Data. Choose `None` if no data is to be sent.
            
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
