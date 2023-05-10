from growcube_parser import GrowcubeParser
import socket

HOST = "172.30.2.202"
PORT = 8800

parser = GrowcubeParser()
data = ""
print(f"Connecting to Growcube at {HOST}")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
    stream.connect((HOST, PORT))
    print("Connected")
    try:
        while True:
            buffer = stream.recv(512)
            data += buffer.decode()
            # print(data)
            if data:
                result = parser.parse_buffer(data)
                data = ""
                # print(result)
                if result is not None:
                    result.dump()
                else:
                    print("ignored")
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        stream.close()
        
    
