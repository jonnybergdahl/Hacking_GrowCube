from growcubereport import *


class GrowcubeParser:
    """This class is  not used
    """

    def __init__(self):
        self.CMD_HEAD = "elea"
        self.CMD_SPLIT = "#"

    def get_command(self, data):
        if data in self.Response:
            return self.Response[data]
        else:
            return "Unknown"

    def parse_buffer(self, buffer):
        index = buffer.find(self.CMD_HEAD)
        if index != -1:
            # print(buffer)
            command = buffer[index + 4: index + 6]
            data = buffer[index + 7:buffer.find(chr(0))]
            print(f"[ {data} ] - ", end='')
            attributes = data.split(self.CMD_SPLIT)

            # print(f"Command: {self.get_command(command)}")
            # for s in attributes:
            #    print(s)
            if command == "20":
                return WaterStateReport(command, attributes)
            elif command == "21":
                return MoistureHumidityStateReport(command, attributes)
            elif command == "23":
                return AutoWaterReport(command, attributes)
            elif command == "24":
                return VersionAndWaterReport(command, attributes)
            else:
                return UnknownReport(command, attributes)
        return None
