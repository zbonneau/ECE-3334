import cv2
import numpy as np
from inference import get_model
import supervision as sv

# Open Camera
camera: cv2.VideoCapture = cv2.VideoCapture(0)
model = get_model(model_id="playing-cards-ow27d/4", api_key="------NO SIR YOU GET NONE OF THIS-----")

# Check for success
if (not camera.isOpened()):
    exit()

# Open Video File
width = int(camera.get(3))
height = int(camera.get(4))
recording = cv2.VideoWriter("DetectPlayingCards.avi",
                            cv2.VideoWriter.fourcc(*'DIVX'),
                            20, (width, height))

while (1):
    # Read frame
    _, frame = camera.read()

    """ *****************************************************
    Title:  Run a Private, Fine-Tuned Model
    Author: Roboflow
    Date:   n.d. (Accessed Aug 31 2024)
    Code Version: No version
    Availability: https://inference.roboflow.com/quickstart/explore_models/#run-a-private-fine-tuned-model 
        *****************************************************"""
    
    # Execute model on frame
    results = model.infer(frame)[0]
    detections = sv.Detections.from_inference(results)
    boxer = sv.BoundingBoxAnnotator()
    noter = sv.LabelAnnotator()
    
    # Draw results on frame
    annotated_image = boxer.annotate(scene=frame, detections=detections)
    annotated_image = noter.annotate(scene=annotated_image, detections=detections)

    # Display frame, save video
    cv2.imshow("Detected Playing Cards", annotated_image)
    recording.write(annotated_image)
    char = (cv2.waitKey(1) & 0xFF)

    if (char == ord('q')):
        break

cv2.destroyAllWindows()   
camera.release()
recording.release()
