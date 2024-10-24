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

1. Create Virtual Environment:
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
sudo python3 greenhouse_main.py
```

## Environmental Parameters

- Temperature Range: 15.5°C - 26.7°C (60°F - 80°F)
- Maximum Humidity: 60%
- Water Detection: Binary (Present/Not Present)

## System Operation

- The system continuously monitors temperature and humidity
- Fan activates when temperature or humidity exceeds thresholds
- Water sensor provides real-time water detection
- All sensor data is logged to the console

## Troubleshooting

If you encounter errors:
1. Check all physical connections
2. Verify virtual environment is activated
3. Confirm all required packages are installed
4. Ensure proper permissions (sudo) when running

## Maintenance

- Regularly check sensor connections
- Clean sensors as needed
- Update threshold values in code if required
- Monitor system logs for any anomalies

## Future Expansions

System is designed for easy expansion with additional modules:
- Soil moisture sensors
- pH monitoring
- Automated watering
- Data logging
- Remote monitoring

For questions or issues, please refer to documentation or raise an issue in the repository.
