echo "killing previous port-forward"
P=$(ps -ax | grep kubectl | grep -v grep | awk '{ print $1 }');for p in ${P[*]}; do kill $p; done
sleep 5
echo "starting new port-forwards"
screen -dm bash -c 'kubectl port-forward --address 0.0.0.0 deploy/inference 3000:3000'
screen -dm bash -c 'kubectl port-forward --address 0.0.0.0 deploy/gps-queue 3001:3000'
sleep 10
echo "loading object detection"
PREDICT_HOST="http://localhost:3000" GPS_QUEUE_HOST="http://localhost:3001" python3 detect.py --model efficientdet_lite0.tflite --cameraId 0 #--enableEdgeTPU
sleep 10
