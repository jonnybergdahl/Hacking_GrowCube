from growcube_client import GrowcubeClient

HOST = "172.30.2.71"
PORT = 8800

print(f"Connecting to Growcube at {HOST}")
client = GrowcubeClient(HOST, PORT)
client.connect()

sent = False
while True:
    message = client.get_next_report()
    if message is not None:
        message.dump()
    #if not sent:
        #client.socket_client.send_message("elea47#3#1@0#")
        #client.socket_client.send_message("elea27#1#1#")

    
