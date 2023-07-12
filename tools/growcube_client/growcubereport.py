class ReportBase:
    Response = {
        20: "RepWaterState",
        21: "RepSTHSate",
        22: "RepCurve",
        23: "RepAutoWater",
        24: "RepVersionAndWater",
        25: "RepErasureData",
        26: "RepPumpOpen",
        27: "RepPumpClose"
    }
    CMD_INNER = "@"

    def __init__(self, command):
        if command in self.Response:
            self.command = self.Response[command]
        else:
            self.command = f"Unknown report: {command}"

    def dump(self):
        print(self.command)


# Response 20 - RepWaterState
class WaterStateReport(ReportBase):
    def __init__(self, data):
        ReportBase.__init__(self, 20)
        self.water_warning = int(data) != 1

    def dump(self):
        print(f"{self.command}: water_warning: {self.water_warning}")


# Response 21 - RepSTHState
class MoistureHumidityStateReport(ReportBase):
    def __init__(self, data):
        ReportBase.__init__(self, 21)
        values = data.split(self.CMD_INNER)
        self.pump = int(values[0])
        self.moisture = int(values[1])
        self.humidity = int(values[2])
        self.temperature = int(values[3])

    def dump(self):
        print(f"{self.command}: pump: {self.pump}, moisture: {self.moisture}, humidity: {self.humidity}, temperature: {self.temperature}")


# Response 23 - AutoWater
class AutoWaterReport(ReportBase):
    def __init__(self, data):
        ReportBase.__init__(self, 23)
        parts = data.split(self.CMD_INNER)
        self.pump = int(parts[0])
        self.year = int(parts[1])
        self.month = int(parts[2])
        self.date = int(parts[3])
        self.hour = int(parts[4])
        self.minute = int(parts[5])

    def dump(self):
        print(f"{self.command}: {self.pump} - {self.year}-{self.month}-{self.date} {self.hour}:{self.minute}")


# Response 24 -
# elea24#11#3.6@2487625#
class VersionAndWaterReport(ReportBase):
    def __init__(self, data):
        ReportBase.__init__(self, 24)
        temp = data.split(self.CMD_INNER)
        self.version = temp[0]

    def dump(self):
        print(f"{self.command}: version {self.version}")


class UnknownReport(ReportBase):
    def __init__(self, command, data):
        ReportBase.__init__(self, command)
        self.data = ", ".join(data)

    def dump(self):
        print(f"{self.command}: data {self.data}")