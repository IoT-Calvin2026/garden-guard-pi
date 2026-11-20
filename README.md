# garden-guard-pi

This repository holds the core Raspberry Pi code for the Garden Guard monitoring system, including simulated Firestore data and the HTTP MJPEG video live stream.

## Vscode PI Setup

- When logged into the pi over SSH, make sure the Remote - SSH extension is installed to develop in vscode.
- When logged in over raspberrypi connect, install the Remote - Tunnels extension and run ```code tunnel``` to start the vscode server. 

## Local Development

Ensure the virtual environment and required packages are installed.
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Next, start the HiveMQ broker in a docker container using and replace EXAMPLE-KEY with your free license key:
```
docker run --name hivemq -p 8080:8080 -p 1883:1883 --pull=always -e HIVEMQ_LICENSE_KEY='EXAMPLE-KEY' -e HIVEMQ_LOG_BASED_CLUSTERING_ENABLED=true   hivemq/hivemq4:latest
```

## Firebase data simulator

The Pi writes random data directly to Firestore without a backend or MQTT
broker. Add `FIREBASE_SERVICE_ACCOUNT=firebase-service-account.json` to `.env`.

The simulator uses only the modeled fields:

- `events`: `eventId`, `createdAt`, `temp`, `nws_conditions`
- `soil_moisture`: `id`, `eventId`, `type`, `soilMoisture`

Create documents interactively:

```
source .venv/bin/activate
python3 firebase_simulator.py
```

The script asks how many Event and Soil Moisture pairs to create.

Create a specific number without a prompt:

```
python3 firebase_simulator.py --create 10
```

Delete a specific number of oldest documents from each collection:

```
python3 firebase_simulator.py --delete 10
```

The script also prints how many documents it deleted. `--delete` with no
number asks for a count interactively.

Clear Event and Soil Moisture collections, including legacy Motion documents:

```
python3 firebase_simulator.py --clear
```

The clear command prints a warning and requires typing `DELETE` before
changes are made. Use `--yes` only for trusted automation.

## Camera

To take a photo, set the DELAY_SECONDS, TOTAL_PHOTOS, and SAVE_DIRECTORY variables in ```delayed_photo.py``` and run the script.