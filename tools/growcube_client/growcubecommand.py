class CommandBase:
    CHD_HEAD = "elea"
    CMD_SET_WORK_MODE = "43"
    CMD_SYNC_TIME = "44"
    CMD_PLANT_END = "45"
    CMD_CLOSE_PUMP = "46"
    CMD_REQ_WATER = "47"
    CMD_REQ_CURVE_DATA = "48"
    MSG_SYNC_WATER_LEVEL = "ele502"
    MSG_SYNC_WATER_TIME = "ele503"
    MSG_DEVICE_UPGRADE = "ele504"
    MSG_FACTORY_RESET = "ele505"

    def __init__(self, command: str, message: str):
        self.command = command;
        self.message = message

    def get_message(self):
        return f"elea{self.command}#{len(self.message)}#{self.message}#"


# Command 43 - SetWorkMode
class SetWorkModeCommand(CommandBase):
    def __init__(self, mode: int):
        super().__init__(self, self.CMD_SET_WORK_MODE, str(mode))


# Command 44 - Sync time
class SyncTimeCommand(CommandBase):
    def __init__(self, timestamp: datetime):
        super().__init__(self, self.CMD_SYNC_TIME, timestamp.strftime("%Y@%m@%d@%H@%M@%S"))  # Java: yyyy@MM@dd@HH@mm@ss


# Command 45 - Plant end ??
class PlantEndCommand(CommandBase):
    def __init__(self, pump: int):
        super().__init__(self, self.CMD_SYNC_TIME, str(pump))


# Command 46 - Close pump
class ClosePumpCommand(CommandBase):
    def __init__(self, pump: int):
        super().__init__(CommandBase.CMD_CLOSE_PUMP, str(pump))


# Command 47 - Water
class WaterCommand(CommandBase):
    def __init__(self, pump: int, state: int):
        super().__init__(CommandBase.CMD_REQ_WATER, f"{pump}#{state}")


# Command 48 - Request curve data
class RequestCurveDataCommand(CommandBase):
    def __init__(self, pump: int):
        super().__init__(CommandBase.CMD_REQ_CURVE_DATA, str(pump))


# Command 49 - Water mode
class WaterModeCommand(CommandBase):
    def __init__(self, pump: int, mode: int, min_value: int, max_value: int):
        super().__init__(self, self.CMD_WATER, f"{pump}@{mode}@{min_value}@{max_value}")


# Command 50 - WiFi settings
class WiFiSettingsCommand(CommandBase):
    def __init__(self, pump: int, mode: int, min_value: int, max_value: int):
        super().__init__(self, self.CMD_WATER, f"{pump}#{mode}#{min_value}#{max_value}")


# Command 502 - Sync water level
class SyncWaterLevelCommand(CommandBase):
    def get_message(self):
        return self.MSG_SYNC_WATER_LEVEL


# Command 503 - Sync water time
class SyncWaterTimeCommand(CommandBase):
    def get_message(self):
        return self.MSG_SYNC_WATER_TIME


# Command 504 - Device upgrade
class SyncDeviceUpgradeCommand(CommandBase):
    def get_message(self):
        return self.MSG_DEVICE_UPGRADE


# Command 505 - Factory reset
class SyncWFactoryResteCommand(CommandBase):
    def get_message(self):
        return self.MSG_FACTORY_RESET