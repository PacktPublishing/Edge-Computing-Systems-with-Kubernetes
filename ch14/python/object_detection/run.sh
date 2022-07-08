screen -dm bash -c 'kubectl port-forward deploy/inference 3000:3000'
screen -dm bash -c 'kubectl port-forward deploy/gps-queue 3001:3000'
sleep 10
PREDICT_HOST="http://localhost:3000" GPS_QUEUE_HOST="http://localhost:3001" python3 detect.py --model efficientdet_lite0.tflite --cameraId 0 --enableEdgeTPU False
