#!/usr/bin/env python3
import importlib
import time
import sys
from globals import glo, DEBUG

def main()->None:
    # List of modules to run - 
    modules = ['greenhouse_dht22', 'greenhouse_fan', 'greenhouse_water_sensor', 'greenhouse_soil_moisture', 'greenhouse_vaporizer', 'greenhouse_pump']
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
    now = time.time()
    try:
        while True:
            nextTime = now + 60 # 1 minute
            # Read sensor data
            glo.realTemp, glo.realHumd = module_instances['greenhouse_dht22'].read_sensor()
            
            # Run fan control and vaproizer with sensor data
            module_instances['greenhouse_fan'].run()
            module_instances['greenhouse_vaporizer'].run()
            
            # Check water sensor
            water_detected = module_instances['greenhouse_water_sensor'].run()
            
            # Check soil moisture sensor
            moisture, soil_temp = module_instances['greenhouse_soil_sensor'].run()

            # run pump if necessary
            if water_detected:
                module_instances['greenhouse_pump'].run()
            elif DEBUG:
                print("Needs more water")
            now = time.time()
            sleepInterval = max(0, nextTime-now)
            time.sleep(sleepInterval)  # Adjust the sleep time as needed
            now = nextTime

    except KeyboardInterrupt:
        print("Greenhouse control terminated by user.")
    finally:
        # Cleanup
        for module_name, module in module_instances.items():
            if hasattr(module, 'cleanup'):
                module.cleanup()
