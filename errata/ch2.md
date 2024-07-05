# Updates in the chapter
### Page N - Title
## Fix Page 33-34 - Creating a single node K3s cluster using Ubuntu OS
2. Once you are logged in, execute the following line in your Terminal to perform a basic installation of K3s:
```
$ curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" INSTALL_K3S_EXEC="--disable traefik --disable=servicelb" sh -s -
```

3. (Optional) If you want to install K3s on AWS Graviton 2 instances or another cloud provider where the public IP is not associated with a network interface in the OS, you have to set the external IP parameter with the public IP of the instance, using the following commands:
```
$ PUBLIC_IP=YOUR_PUBLIC_IP|YOUR_PRIVATE_IP
$ curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" INSTALL_K3S_EXEC="--disable traefik --tls-san "$PUBLIC_IP" --node-external-ip="$PUBLIC_IP" --node-ip="$PUBLIC_IP" --disable=servicelb" sh -s -
```

## Fix Page 35 - Adding more nodes to your K3s cluster for multi-node configuration
6. Register your node using the following command:
```
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="agent --server https://MASTER_PUBLIC_OR_PRIVATE_IP:6443 --token ${TOKEN} --with-node-id" sh -s -
```