cp traffic.desktop /home/$USER/Desktop
#cp *.desktop /home/$USER/Desktop
cat <<EOF > /home/$USER/Desktop/detector.desktop
[Desktop Entry]
Comment=Detector
Terminal=true
Name=Detector
Exec=/bin/bash /home/$USER/Edge-computing-with-K3os-and-k3s/ch14/code/python/object_detection/run.sh
Type=Application
Icon=/usr/share/pixmaps/chromium-browser.png
Path=/home/$USER/Edge-computing-with-K3os-and-k3s/ch14/code/python/object_detection
EOF

cat <<EOF > /home/$USER/Desktop/kill.desktop
[Desktop Entry]
Comment=Kill
Terminal=true
Name=Kill
Exec=/bin/bash /home/sergioarmgpl/Edge-computing-with-K3os-and-k3s/ch14/code/python/object_detection/kill.sh
Type=Application
Icon=/usr/share/pixmaps/chromium-browser.png
Path=/home/sergioarmgpl/Edge-computing-with-K3os-and-k3s/ch14/code/python/object_detection
EOF