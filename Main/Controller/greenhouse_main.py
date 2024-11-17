#!/usr/bin/env python3
import importlib
import time
import sys
from globals import glo, DEBUG, CHECK_INTERVAL

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
    nextTime = now + CHECK_INTERVAL # 1 minute
    try:
        while not glo.closeApplication:
            now = time.time()
            sleepInterval = max(0, nextTime-now)
            time.sleep(sleepInterval)  # Adjust the sleep time as needed
            nextTime += CHECK_INTERVAL
            # Read sensor data
            glo.realTemp, glo.realHumd = module_instances['greenhouse_dht22'].read_sensor()
            # Check soil moisture sensor
            moisture, soil_temp = module_instances['greenhouse_soil_moisture'].run()
            
            # Check water sensor
            water_detected = module_instances['greenhouse_water_sensor'].run()
            try:
                message =  "===== Sensor Values ==============\n"
                message += f" TEMP:  {glo.realTemp:.1f}\n"
                message += f" HUMD:  {glo.realHumd:.1f}\n"
                message += f" Moist: {glo.realMoist:.1f}\n"
                if not water_detected:
                    message += "Warning: Needs Water. Please Refill\n\n"

                print(message)
            except Exception:
                continue
            # Run fan control and vaproizer with sensor data
            module_instances['greenhouse_fan'].run()
            module_instances['greenhouse_vaporizer'].run()
            

            # run pump if necessary
            if water_detected:
                module_instances['greenhouse_pump'].run()
                pass
            elif DEBUG:
                print("Needs more water")


    except KeyboardInterrupt:
        print("Greenhouse control terminated by user.")
    finally:
        # Cleanup
        for module_name, module in module_instances.items():
            if hasattr(module, 'cleanup'):
                module.cleanup()


if __name__ == "__main__":
    DEBUG = True
    main()