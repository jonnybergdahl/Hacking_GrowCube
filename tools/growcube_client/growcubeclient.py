from growcube_client.crowcubesocketclient import GrowcubeSocketClient
from growcube_client.growcubereport import *


class GrowcubeClient:
    def __init__(self, host: str, port: str):
        self.socket_client = GrowcubeSocketClient(host, port)

    def connect(self):
        self.socket_client.connect()

    def disconnect(self):
        self.socket_client.disconnect()

    def get_next_report(self):
        message = self.socket_client.receive_message()
        if message is not None:
            print(message.message)
            if message.command == 20:
                return WaterStateReport(message.payload)
            elif message.command == 21:
                return MoistureHumidityStateReport(message.payload)
            elif message.command == 23:
                return AutoWaterReport(message.payload)
            elif message.command == 24:
                return VersionAndWaterReport(message.payload)
            else:
                return UnknownReport(message.command, message.payload)
