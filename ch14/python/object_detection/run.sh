
screen -dm bash -c 'kubectl port-forward deploy/inference 3000:3000'
sleep 10
PREDICT_HOST="http://localhost:3000" python3 detect.py --model efficientdet_lite0.tflite --cameraId 0
