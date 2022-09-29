cp traffic.desktop /home/$USER/Desktop
#cp *.desktop /home/$USER/Desktop
cat <<EOF > /home/$USER/Desktop
[Desktop Entry]
Comment=Detector
Terminal=true
Name=Detector
Exec=/bin/bash /home/$USER/Edge-computing-with-K3os-and-k3s/ch14/code/python/object_detection/run.sh
Type=Application
Icon=/usr/share/pixmaps/chromium-browser.png
Path=/home/$USER/Edge-computing-with-K3os-and-k3s/ch14/code/python/object_detection
EOF