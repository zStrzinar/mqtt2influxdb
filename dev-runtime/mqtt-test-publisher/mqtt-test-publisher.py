import sys, os, time, datetime
import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

if __name__ == "__main__":
    print("Hello World!")
    
    print(" ".join(sys.argv))
    assert len(sys.argv) == 4

    host_port: str = sys.argv[1]
    host_port = host_port.split(":")
    host: str = host_port[0]
    port: int = int(host_port[1])

    topic: str = sys.argv[2]

    file: str = sys.argv[3]

    print(host)
    print(port)
    print(topic)
    print(file)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    for i in range(10):
        try:
            client.connect(host, port, 60)
            break
        except :
            time.sleep(min(pow(2,i), 120))
            pass

    with open(file, "r") as f:
        while True:
            message: str = f.readline() # TODO: check if end of file is reached, and circle back
            client.publish(topic, message) 
            print(f"Published message {message}")
            time.sleep(1)

    exit(0)

