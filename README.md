# 🌡️ IoT Cold Chain Sensor Logger

> ESP32-style IoT sensor simulator with real-time anomaly detection and data logging — built around cold chain dairy transport constraints.

---

## Overview

This project simulates an ESP32-based cold chain monitoring system for dairy transportation. It generates realistic temperature and humidity sensor readings, detects threshold violations in real time, logs all data to file, and supports loading and analysis of historical readings.

Built in Python using object-oriented design, it mirrors the architecture of a real-world IoT monitoring pipeline — where ESP32 nodes publish sensor data via MQTT to a backend system that logs, analyses, and alerts on anomalies.

---

## Background

Cold chain logistics for dairy products requires continuous environmental monitoring throughout transportation. Temperature deviations — even brief ones — can compromise product safety and result in significant losses. This project replicates the data pipeline layer of such a system, simulating the kind of readings an ESP32 microcontroller would publish over MQTT in a real deployment.

---

## Features

- Simulates multiple ESP32 sensor nodes with realistic temperature and humidity data
- 15% randomised anomaly injection to mimic real sensor fault conditions
- Real-time threshold violation detection with configurable safe zones
- Alert generation with detailed violation messages
- CSV-style data logging to file
- Full data reload and reconstruction from log file
- Statistical summary — min, max, average across all readings
- Threshold-based filtering for post-trip analysis

---

## Cold Chain Thresholds

| Parameter   | Safe Range     |
|-------------|----------------|
| Temperature | 2.0°C — 8.0°C  |
| Humidity    | 40.0% — 80.0%  |

These values reflect standard dairy transportation requirements. Both limits are configurable as class variables in `SensorLogger`.

---

## Project Structure

```
cold-chain-logger/
│
├── sensor_logger.py       # Main source file
├── cold_chain_log.txt     # Auto-generated log file (created on first run)
└── README.md
```

---

## How It Works

```
simulate_esp32_data()
        │
        ▼
SensorReading objects created
        │
        ▼
logger.add_reading(reading)
        │
        ├──► _check_anomaly() ──► Alert if threshold violated
        │
        └──► readings[] list
                │
                ▼
        save_to_file() ──► cold_chain_log.txt
                │
                ▼
        load_from_file() ──► Reconstruct readings
                │
                ▼
        above_threshold() / summary()
```

---

## Getting Started

### Requirements

- Python 3.8+
- No external libraries required — standard library only

### Run

```bash
git clone https://github.com/yourusername/cold-chain-logger.git
cd cold-chain-logger
python sensor_logger.py
```

### Sample Output

```
=== IoT Cold Chain Sensor Logger ===

📡 Simulating ESP32-01...
  [2025-04-03 10:30:01] Sensor ESP32-01 | Temp: 4.7°C | Humidity: 63.2%
  [2025-04-03 10:30:01] Sensor ESP32-01 | Temp: 9.3°C | Humidity: 58.1%
  ⚠️  ALERT: Temp TOO HIGH (9.3°C > 8.0°C)
  [2025-04-03 10:30:01] Sensor ESP32-01 | Temp: 3.1°C | Humidity: 88.4%
  ⚠️  ALERT: Humidity TOO HIGH (88.4% > 80.0%)

📊 --- Summary ---
  Total readings : 16
  Temp  — Min: 1.2°C | Max: 9.3°C | Avg: 5.1°C
  Humid — Min: 37.4% | Max: 88.4% | Avg: 61.7%
  Alerts generated: 3

✅ Saved 16 readings to 'cold_chain_log.txt'
```

---

## Extending to Real Hardware

This project is designed to be a drop-in analytics layer for a real ESP32 deployment. To switch from simulated to live data, replace the simulation function with one of the following:

### Option 1 — Load from existing CSV log
```python
readings = load_from_csv("esp32_data.csv")
for r in readings:
    logger.add_reading(r)
```

### Option 2 — Live MQTT stream (real deployment)
```python
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    parts = msg.payload.decode().split(",")
    reading = SensorReading("ESP32-01", float(parts[0]), float(parts[1]))
    userdata.add_reading(reading)

client = mqtt.Client(userdata=logger)
client.on_message = on_message
client.connect("your_broker_ip", 1883)
client.subscribe("coldchain/sensor1")
client.loop_forever()
```

---

## OOP Concepts Demonstrated

| Concept | Where Used |
|---|---|
| `__init__` | Both classes — object initialisation |
| `__str__` | Human-readable print output |
| `__repr__` | Developer/debug representation |
| `__eq__` | Meaningful object comparison |
| `__len__` | `len(logger)` support |
| `__iter__` | `for reading in logger` support |
| Class variables | Shared threshold constants |
| Private methods | `_check_anomaly()` — internal use only |
| `with` statement | Safe file open/close via context manager |

---

## Real-World Counterpart

This project mirrors the software layer of an actual IoT cold chain system built using:

- **ESP32** microcontroller with DHT22 temperature/humidity sensor
- **SIM800L** GSM module for remote data transmission
- **GPS module** for location tracking
- **MQTT protocol** for lightweight publish/subscribe messaging

The hardware system publishes readings to an MQTT broker. This Python logger represents the backend analytics layer that would consume, validate, and store those readings.

---

## Author

**Jay** 

Interests: Embedded Systems · IoT · Automotive Firmware · Cold Chain Logistics · Software Development 

--
