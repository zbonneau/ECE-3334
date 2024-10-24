# Greenhouse Control System

A Raspberry Pi-based system for monitoring and controlling a greenhouse environment. This system includes temperature, humidity, and water detection monitoring, along with automated fan control.

## Components

- DHT22 Temperature/Humidity Sensor
- Water Detection Sensor
- Fan Control System
- Raspberry Pi (any model)

## Pin Configuration

### DHT22 Sensor
- VCC → 3.3V/5V power
- GND → Ground
- DATA → GPIO4 (Pin 7)

### Water Sensor
- VCC → 5V power
- GND → Ground
- OUT → GPIO17 (Pin 11)

### Fan Control
- VCC → Fan power (5V/12V)
- GND → Ground
- Control → GPIO14 (Pin 8)

## Files and Their Functions

### `greenhouse_main.py`
- Main control script
- Coordinates all sensor modules
- Manages system initialization and cleanup

### `greenhouse_dht22.py`
- Controls DHT22 temperature/humidity sensor
- Provides temperature and humidity readings
- Manages sensor timing and error handling

### `greenhouse_water_sensor.py`
- Monitors water presence
- Reports water detection status
- Handles sensor initialization and cleanup

### `greenhouse_fan.py`
- Controls fan operation
- Responds to temperature/humidity readings
- Manages fan state based on environmental conditions

## Setup Instructions

1. Create Virtual Environment(It has already been created):
```bash
python3 -m venv greenhouse_env
```

2. Activate Virtual Environment:
- Linux/Mac:
```bash
source greenhouse_env/bin/activate
```
- Windows:
```bash
greenhouse_env\Scripts\activate
```

3. Install Required Packages:
```bash
pip3 install adafruit-circuitpython-dht
pip3 install RPi.GPIO
```

4. Make Scripts Executable:
```bash
chmod +x greenhouse_main.py
chmod +x greenhouse_dht22.py
chmod +x greenhouse_water_sensor.py
chmod +x greenhouse_fan.py
```

## Running the System

1. Ensure your virtual environment is activated
2. Run the main script:
```bash
python3 greenhouse_main.py
```

## Environmental Parameters

- Temperature Range: 15.5°C - 26.7°C (60°F - 80°F)
- Maximum Humidity: 60%
- Water Detection: Binary (Present/Not Present)
