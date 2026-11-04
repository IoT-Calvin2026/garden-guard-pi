import json
import time
import psutil
import paho.mqtt.client as paho

BROKER_HOST = "127.0.0.1" # laptop IP address that is running docker container
PORT = 1883
TOPIC = "local/pi/health"

# assign connection acknowledgement callback
def on_connect(client, userdata, flags, reason_code, properties):
    print('CONNACK received: %s' % (reason_code))

# create a client
client = paho.Client(paho.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

# connect to the broker
print(f"Connecting to local broker at {BROKER_HOST}:{PORT}...")
client.connect(BROKER_HOST, PORT, keepalive=60)

# begin publishing health data
try:
    print("Beginning local publisher loop. Press Ctrl+C to stop.")
    while True:
        payload = {
            "timestamp": int(time.time()),
            "mem_used": f"{psutil.virtual_memory().percent} %",
            "status": "local_dev"
        }
        
        # Publish payload string
        client.publish(TOPIC, json.dumps(payload), qos=0)
        print(f"Sent: {payload}")
        
        time.sleep(5)  # Send metrics every 5 seconds

except KeyboardInterrupt:
    print("\nDisconnecting from local broker...")
    client.disconnect()

