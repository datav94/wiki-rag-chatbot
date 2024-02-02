### Login
az login --tenant adpvwg.onmicrosoft.com

### Set the subscription context
az account set --subscription CARIAD.g3-adp-groupmdm.adp-groupmdm-dev-001

### Get the credentials for the specific AKS cluster
az aks get-credentials -g natural-language-interface -n aks-nli-ray --overwrite-existing

### Create and attach a nodepool to the cluster

az aks nodepool add --resource-group natural-language-interface --cluster-name aks-nli-ray --name gpuray --node-count 3 --node-vm-size Standard_NC12s_v3 --node-taints sku=gpu:NoSchedule --aks-custom-headers UseGPUDedicatedVHD=true --enable-cluster-autoscaler --min-count 3 --max-count 5

### Aftre successful creation, install KubeRay on this cluster using helm
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update
helm install kuberay-operator kuberay/kuberay-operator --version 1.0.0


### Intsall Ray Service
kubectl apply -f ray-service.llama7b.yaml

### Check if service is up and running, it takes 5 to 10 mins
kubectl get services

### Expose Service on external IP
kubectl expose service code-llama-serve-svc --type=LoadBalancer --name codellama-loadbalancer

### Check the external IP and test the services
```python 
import requests
import time

response = requests.post("URL", params={"text": "def minhash(arr "})
print(response.json())

```

###Please note that both the service & the code llama model is uploaded to a azure storage account

#### Zip the code and upload it to azure storage container and set the URL in the yaml file with SAS token

#### Similarly generate the URL with SAS token for model as well, which goes inside the code. This can also be done with mounting the file





