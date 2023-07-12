class GrowcubeMessage:
    """ Main message type abstraction.
    """
    HEADER = 'elea'
    DELIMITER = '#'
    END_DELIMITER = '#'
    EMPTY_MESSAGE = HEADER + "00" + DELIMITER + DELIMITER + DELIMITER

    def __init__(self, message, command, payload):
        self.message = message
        self.command = command
        self.payload = payload

    # This function returns the index of the non consumed data in the buffer,
    # together with the message
    @staticmethod
    def from_bytes(data: bytearray):
        """Converts a byte array to a GrowcubeMessage instance
        """
        command = None
        payload = None
        message_str = data.decode('utf-8')

        start_index = message_str.find(GrowcubeMessage.HEADER)
        if start_index == -1:
            print("Header not found, exiting")
            return 0, None

        # Move to start of message
        message_str = message_str[start_index:]
        #print(f"message_str is now {message_str}")

        parts = message_str[len(GrowcubeMessage.HEADER):].split(GrowcubeMessage.DELIMITER)
        if len(parts) < 3:
            # Still don't have the complete message
            print(f"Got parts: {parts}")
            return start_index, None

        try:
            payload_len = int(parts[1])
        except ValueError:
            raise ValueError('Invalid payload length')

        payload = parts[2]
        payload_length = len(GrowcubeMessage.EMPTY_MESSAGE) + len(str(payload_len)) + len(payload)
        consumed_index = start_index + payload_length
        if len(data) < consumed_index:
            # Still incomplete
            return start_index, None

        if not message_str[payload_length - 1] == GrowcubeMessage.DELIMITER:
            raise ValueError('Invalid message end delimiter')

        try:
            command = int(parts[0])
        except ValueError:
            raise ValueError('Invalid command')

        return consumed_index, GrowcubeMessage(data[start_index:consumed_index], command, payload)

    def to_bytes(self, command: int, data: str):
        """Converts a GrowcubeMessage instance to a bytearray
        """
        result =f"{GrowcubeMessage.HEADER}{command:02d}{GrowcubeMessage.DELIMITER}{len(data)}" + \
                f"{GrowcubeMessage.DELIMITER}{data}{GrowcubeMessage.DELIMITER}"
        return result.encode()
