# Greenhouse Control System
A Raspberry Pi-based system for monitoring and controlling a greenhouse environment. This system includes temperature, humidity, water detection monitoring, automated fan control, soil moisture monitoring, and humidity control via vaporizer.

## Components
* DHT22 Temperature/Humidity Sensor
* Water Detection Sensor
* Fan Control System
* Soil Moisture Sensor (Adafruit STEMMA)
* USB Vaporizer
* Raspberry Pi (any model)

## Pin Configuration

### DHT22 Sensor
* VCC → 3.3V/5V power
* GND → Ground
* DATA → GPIO4 (Pin 7)

### Water Sensor
* VCC → 5V power
* GND → Ground
* OUT → GPIO17 (Pin 11)

### Fan Control
* VCC → Fan power (5V/12V)
* GND → Ground
* Control → GPIO14 (Pin 8)

### Soil Moisture Sensor
* VCC → 3.3V power (Blue)
* GND → Ground (Green)
* SDA → I2C SDA (Orange, pin 3)
* SCL → I2C SCL (Red, pin 5)

### Vaporizer
* GPIO 22 (Pin 15)

### Pump 
* GPIO 27 (Pin 13)
* Blue = Negative 
* Brown = Pos
* Yellow = GND (DISCONNECTED)

## Files and Their Functions

`greenhouse_main.py`
* Main control script
* Coordinates all sensor modules
* Manages system initialization and cleanup

`greenhouse_dht22.py`
* Controls DHT22 temperature/humidity sensor
* Provides temperature and humidity readings
* Manages sensor timing and error handling

`greenhouse_water_sensor.py`
* Monitors water presence
* Reports water detection status
* Handles sensor initialization and cleanup

`greenhouse_fan.py`
* Controls fan operation
* Responds to temperature/humidity readings
* Manages fan state based on environmental conditions

`greenhouse_soil_sensor.py`
* Monitors soil moisture and temperature
* Uses Adafruit STEMMA sensor
* Provides continuous soil condition monitoring

`greenhouse_vaporizer.py`
* Controls USB vaporizer
* Manages humidity through vaporization
* Handles USB communication and device state

## Setup Instructions

1. Create Virtual Environment(It has already been created):
```
python3 -m venv greenhouse_env
```

2. Activate Virtual Environment:
* Linux/Mac:
```
source greenhouse_env/bin/activate
```
* Windows:
```
greenhouse_env\Scripts\activate
```

3. Install Required Packages:
```
pip3 install adafruit-circuitpython-dht
pip3 install RPi.GPIO
pip3 install adafruit-circuitpython-seesaw
pip3 install pyserial
```

4. Make Scripts Executable:
```
chmod +x greenhouse_main.py
chmod +x greenhouse_dht22.py
chmod +x greenhouse_water_sensor.py
chmod +x greenhouse_fan.py
chmod +x greenhouse_soil_sensor.py
chmod +x greenhouse_vaporizer.py
```

## Running the System
1. Ensure your virtual environment is activated
2. Run the main script:
```
python3 greenhouse_main.py
```

## Environmental Parameters
* Temperature Range: 15.5°C - 26.7°C (60°F - 80°F)
* Maximum Humidity: 60%
* Water Detection: Binary (Present/Not Present)
* Soil Moisture: 0-100%
* Soil Temperature: 0-50°C

