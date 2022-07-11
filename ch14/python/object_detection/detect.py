# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main script to run the object detection routine."""
import argparse
import sys
import time
from collections import Counter

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils
import os

import requests

obj_values = {"car":1,"cat":2,"person":3,"dog":4,"semaphore":5,"other":6}


def run(model: str, camera_id: int, width: int, height: int, num_threads: int,
        enable_edgetpu: bool) -> None:
  """Continuously run inference on images acquired from the camera.

  Args:
    model: Name of the TFLite object detection model.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
    num_threads: The number of CPU threads to run the model.
    enable_edgetpu: True/False whether the model is a EdgeTPU model.
  """

  # Variables to calculate FPS
  counter, fps = 0, 0
  start_time = time.time()

  # Start capturing video input from the camera
  cap = cv2.VideoCapture(camera_id)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  # Visualization parameters
  row_size = 20  # pixels
  left_margin = 24  # pixels
  text_color = (0, 0, 255)  # red
  font_size = 1
  font_thickness = 1
  fps_avg_frame_count = 10

  # Initialize the object detection model
  base_options = core.BaseOptions(
      file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
  detection_options = processor.DetectionOptions(
      max_results=8, score_threshold=0.3)
  options = vision.ObjectDetectorOptions(
      base_options=base_options, detection_options=detection_options)
  detector = vision.ObjectDetector.create_from_options(options)

  # Continuously capture images from the camera and run inference
  items = []
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      sys.exit(
          'ERROR: Unable to read from webcam. Please verify your webcam settings.'
      )

    counter += 1
    image = cv2.flip(image, 1)

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)
#    print(str(detection_result))
#    print(str(len(detection_result.detections)))
#    print(type(detection_result))

    items.clear()


    for detected_obj in detection_result.detections:
#      print("Detected: "+str(detected_obj.classes[0].class_name))
      items.append(str(detected_obj.classes[0].class_name))
    

    print("items",items)
    # Draw keypoints and edges on input image
    image = utils.visualize(image, detection_result)

    # Calculate the FPS
    if counter % fps_avg_frame_count == 0:
      end_time = time.time()
      fps = fps_avg_frame_count / (end_time - start_time)
      start_time = time.time()

    # Show the FPS
    fps_text = 'FPS = {:.1f}'.format(fps)
    text_location = (left_margin, row_size)
    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                font_size, text_color, font_thickness)

#    fps_text = 'Hello my friend'
#    text_location = (left_margin, row_size*2)
#    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
#                font_size, text_color, font_thickness)

    r = 2
    counts = Counter(items)
    print("counts",counts)
#    i = 0
    warning_pred = 0
    found = ""
    warning = 0
    for c in counts:
#        print(c,counts[c])
        fps_text = c + " = " + str(counts[c])
        print("fps_text",fps_text)
        
        object_id = 6
        if c in obj_values:
            object_id = obj_values[c]
        data = {"data":[object_id]}
        headers={"Content-Type":"application/json"}
        r = requests.post(os.environ['PREDICT_HOST']
            + f"/predict",json=data)
        print("warning prediction",r.json()["prediction"])
        warning_pred = int(r.json()["prediction"])

        if warning_pred <=2:
            warning += 1
            found += c + ","
            #record traffic event
            data = {'object':c,
            'warning':warning_pred}
            print("Data",data,file=sys.stderr)
            while True:
              try:
                headers={"Content-Type":"application/json"}
                r = requests.post(os.environ['GPS_QUEUE_HOST']
                + "/traffic/event",json=data)
                print("Response",r.json(),file=sys.stderr)
                break
              except:
                print({"queue_call":"failed"},file=sys.stderr)
                time.sleep(3)
#        text_location = (left_margin, row_size*(i+2))
#        cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
#                    font_size, text_color, font_thickness)
#        i+=1
	
    if warning:
        start_point = (200, 400)
# Ending coordinate, here (220, 220)
# represents the bottom right corner of rectangle
        end_point = (440, 440)
        color = (255, 0, 0)
        thickness = -1
        cv2.rectangle(image, start_point, end_point, color, thickness)
        text_location = (left_margin, row_size*(7))
        cv2.putText(image, found[:-1] + " found", (230, 420), cv2.FONT_HERSHEY_PLAIN,
                    font_size, (255,255,0), font_thickness)
    else:
        start_point = (200, 400)
# Ending coordinate, here (220, 220)
# represents the bottom right corner of rectangle
        end_point = (440, 440)
        color = (255, 0, 0)
        thickness = -1
        cv2.rectangle(image, start_point, end_point, color, thickness)
        text_location = (left_margin, row_size*(7))
        cv2.putText(image, "No warnings", (230, 420), cv2.FONT_HERSHEY_PLAIN,
                    font_size, (255,255,0), font_thickness)


#        warning = False
#        pos = getGPSCoordinate()
#        data = {'lat': pos["lat"],
#        'lng':pos["lng"],
#        'object':object_name}
#        headers={"Content-Type":"application/json"}
#        r = requests.post(os.environ['ENDPOINT']
#            + f"/traffic/object/position",json=data)


    # Stop the program if the ESC key is pressed.
    if cv2.waitKey(1) == 27:
      break
    cv2.imshow('object_detector', image)

  cap.release()
  cv2.destroyAllWindows()


def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      default='efficientdet_lite0.tflite')
  parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, type=int, default=0)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      type=int,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      type=int,
      default=480)
  parser.add_argument(
      '--numThreads',
      help='Number of CPU threads to run the model.',
      required=False,
      type=int,
      default=4)
  parser.add_argument(
      '--enableEdgeTPU',
      help='Whether to run the model on EdgeTPU.',
      action='store_true',
      required=False,
      default=False)
  args = parser.parse_args()

  run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,
      int(args.numThreads), bool(args.enableEdgeTPU))


if __name__ == '__main__':
  main()
