# Updates in the chapter
### Page N - Title
## Fix Page 49-51 - Installing MetalLB

2. Install K3s using the following line. This applies to a simple ARM device for a basic installation without installing KlipperLB:
```
$ curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" INSTALL_K3S_EXEC="--disable traefik --disable=servicelb" sh -s -
```
Then, use the next lines to install K3s in a node that has a public IP:
```
$ curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" INSTALL_K3S_EXEC="--disable traefik --tls-san "$PUBLIC_IP" --node-external-ip="$PUBLIC_IP" --node-ip="$PUBLIC_IP" --disable=servicelb" sh -s -
```

Now the commands to install MetalLB are:
```
$ kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.4/config/manifests/metallb-native.yaml
kubectl get pods -n metallb-system
```
The strictARP just for Kubernetes that uses kube-proxy
See what changes would be made, returns nonzero returncode if different:
```
kubectl get configmap kube-proxy -n kube-system -o yaml | \
sed -e "s/strictARP: false/strictARP: true/" | \
kubectl diff -f - -n kube-system
```
Actually apply the changes, returns nonzero returncode on errors only
```
kubectl get configmap kube-proxy -n kube-system -o yaml | \
sed -e "s/strictARP: false/strictARP: true/" | \
kubectl apply -f - -n kube-system
```
Finally create a range of IP to serve the LoadBalancer:
```
cat <<EOF | kubectl create -f -
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
  - 192.168.1.240-192.168.1.250
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: example
  namespace: metallb-system
EOF
```