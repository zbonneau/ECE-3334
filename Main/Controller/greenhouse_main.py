#!/usr/bin/env python3
import importlib
import time
import sys
from globals import glo
# List of modules to run - , 'greenhouse_soil_moisture', 'greenhouse_vaporizer'
modules = ['greenhouse_dht22', 'greenhouse_fan', 'greenhouse_water_sensor']
# Import modules dynamically
module_instances = {}
for module in modules:
    try:
        module_instances[module] = importlib.import_module(module)
        print(f"Loaded module: {module}")
    except ImportError as e:
        print(f"Error loading module {module}: {e}")
        sys.exit(1)
# Initialize all modules
for module_name, module in module_instances.items():
    if hasattr(module, 'initialize'):
        module.initialize()
try:
    while True:
        # Read sensor data
        glo.realTemp, glo.realHumd = module_instances['greenhouse_dht22'].read_sensor()
        
        # Run fan control with sensor data
        module_instances['greenhouse_fan'].run()
        
        # Check water sensor
        water_detected = module_instances['greenhouse_water_sensor'].run()
        
        # Check soil moisture sensor
        # moisture, soil_temp = module_instances['greenhouse_soil_sensor'].run()
        
        # Run vaporizer control
        # module_instances['greenhouse_vaporizer'].run()
        
        time.sleep(10)  # Adjust the sleep time as needed
except KeyboardInterrupt:
    print("Greenhouse control terminated by user.")
finally:
    # Cleanup
    for module_name, module in module_instances.items():
        if hasattr(module, 'cleanup'):
            module.cleanup()
