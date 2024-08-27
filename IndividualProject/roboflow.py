import cv2
import numpy as np
from inference import get_model
import supervision as sv


camera: cv2.VideoCapture = cv2.VideoCapture(0)
model = get_model(model_id="playing-cards-ow27d/4", api_key="------NO SIR YOU GET NONE OF THIS-----")


if (not camera.isOpened()):
    exit()

width = int(camera.get(3))
height = int(camera.get(4))
recording = cv2.VideoWriter("DetectPlayingCards.avi",
                            cv2.VideoWriter.fourcc(*'DIVX'),
                            20, (width, height))

while (1):
    _, frame = camera.read()

    #print(np.shape(frame))
    results = model.infer(frame)[0]
    detections = sv.Detections.from_inference(results)
    boxer = sv.BoundingBoxAnnotator()
    noter = sv.LabelAnnotator()
    annotated_image = boxer.annotate(
        scene=frame, detections=detections
    )
    annotated_image = noter.annotate(
        scene=annotated_image, detections=detections
    )



    
    cv2.imshow("Detected Playing Cards", annotated_image)
    recording.write(annotated_image)
    char = (cv2.waitKey(1) & 0xFF)

    if (char == ord('q')):
        break

cv2.destroyAllWindows()   
camera.release()
recording.release()
