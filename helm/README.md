## Helm chart for running mnemic in Kubernetes

More info on Mnemic can be found here: https://mnemic.readthedocs.io/en/main/index.html

## Deploying mnemic to Kubernetes

# Initial setup steps:
1. Make sure you are connected to VPN.
2. Make sure your kubectl points to a dev cluster: `kubectl config use-context kops-gaia-dev-mco-us-east-1`

For first time installation only, run:
### For first time installation only, run:
```
helm install \
--name mnemic \
--namespace mnemic \
--set frontend.image.tag=latest \
--set backend.image.tag=latest \
--debug .
```

### To upgrade existing deployment, run:
```
helm upgrade \
--namespace mnemic \
--debug mnemic .
```
