import pprint


class ReportBase:
    Response = {
        "20": "RepWaterState",
        "21": "RepSTHSate",
        "22": "RepCurve",
        "23": "RepAutoWater",
        "24": "RepVersionAndWater",
        "25": "RepErasureData",
        "26": "RepPumpOpen",
        "27": "RepPumpClose"
    }
    CMD_INNER = "@"

    def __init__(self, command):
        if command in self.Response:
            self.command = self.Response[command]
        else:
            self.command = f"Unknown report: {command}"

    def dump(self):
        print(self.command)


# Command 20 - RepWaterState
class RepWaterState(ReportBase):
    def __init__(self, command, data):
        ReportBase.__init__(self, command)
        self.water_warning = int(data[1]) != 1

    def dump(self):
        print(f"{self.command}: water_warning: {self.water_warning}")


# Command 21 - RepSTHState
class RepSTHState(ReportBase):
    def __init__(self, command, data):
        ReportBase.__init__(self, command)
        values = data[1].split(self.CMD_INNER)
        self.pump = int(values[0])
        self.sh = int(values[1])
        self.th = int(values[2])
        self.temperature = int(values[3])

    def dump(self):
        print(f"{self.command}: pump: {self.pump}, sh: {self.sh}, th: {self.th}, temperature: {self.temperature}")


# Command 23 - AutoWater
class AutoWaterReport(ReportBase):
    def __init__(self, command, data):
        ReportBase.__init__(self, command)
        self.pump = int(data[0])
        self.year = int(data[1])
        self.month = int(data[2])
        self.date = int(data[3])
        self.hour = int(data[4])
        self.minute = int(data[5])

    def dump(self):
        print(f"{self.command}: {self.pump} - {self.year}-{self.month}-{self.date} {self.hour}:{self.minute}")


# Command 24 -
# elea24#11#3.6@2487625#
class RepVersionAndWaterReport(ReportBase):
    def __init__(self, command, data):
        ReportBase.__init__(self, command)
        temp = data[1].split(self.CMD_INNER)
        self.version = temp[0]

    def dump(self):
        print(f"{self.command}: version {self.version}")


class UnknownReport(ReportBase):
    def __init__(self, command, data):
        ReportBase.__init__(self, command)
        self.data = ", ".join(data)

    def dump(self):
        print(f"{self.command}: data {self.data}")

class GrowcubeParser:

    def __init__(self):
        self.CMD_HEAD = "elea"
        self.CMD_SPLIT = "#"
        self.CMD_INNER = "@"

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
                return RepWaterState(command, attributes)
            elif command == "21":
                return RepSTHState(command, attributes)
            elif command == "23":
                return AutoWaterReport(command, attributes)
            elif command == "24":
                return RepVersionAndWaterReport(command, attributes)
            else:
                return UnknownReport(command, attributes)
        return None
