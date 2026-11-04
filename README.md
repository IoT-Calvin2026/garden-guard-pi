# garden-guard-pi

This repository holds the core Raspberry Pi code for Garden Guard monitoring system that publishes live telemetry data over MQTT from edge sensors, posts historical event data to the database, and streams a HTTP MJPEG video live stream to the frontend.

## Vscode PI Setup

- When logged into the pi over SSH, make sure the Remote - SSH extension is installed to develop in vscode.
- When logged in over raspberrypi connect, install the Remote - Tunnels extension and run ```code tunnel``` to start the vscode server. 

## Local Development

Ensure virtual environment and required packages (like paho-mqtt) are installed.
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Next, start the HiveMQ broker in a docker container using and replace EXAMPLE-KEY with your free license key:
```
docker run --name hivemq -p 8080:8080 -p 1883:1883 --pull=always -e HIVEMQ_LICENSE_KEY='EXAMPLE-KEY' -e HIVEMQ_LOG_BASED_CLUSTERING_ENABLED=true   hivemq/hivemq4:latest
```