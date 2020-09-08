# Kubernetes Ingress Controller

##  Overview

Ingress provides external access to services in a cluster and can provide load balancing, SSL termination and name-based virtual hosting.

For ingress to route external HTTP traffic an ingress controller must be instantiated in a cluster.

We support two types of ingress controllers:

1. Traefik
2. ingress-nginx

Both types of ingress controller are managed and configured through our common service model.

## Choice of Ingress Controllers

Admins are free to choose ingress-nginx or Traefik if applications require that particular ingress controller.

Ingress controllers can be enabled on a per project basis. However since ingress controller binds to host port 80, 443 and in case of Traefik 8081, there can only be one type of ingress controller deployed on a service domain. Alerts will be raised for conflicting ingress controller types across projects on same service doamin.
You can use the kps CLI to enable or disable an active ingress controller on a project. This is similar to the workflow in the UI:

Enable ingress controller Traefik in project MyProject

```
$ kps service enable traefik -p MyProject
```

Switch to ingress-nginx

```
$ kps service disable traefik -p MyProject
$ kps service enable ingress-nginx -p MyProject
```

Note: Changing ingress controller might affect running applications if ingress routes have already been configured.

## Utilize Ingress from Kubernetes Applications

We provide two ways for applications to define ingress routes. 

1. Annotations on service resources.
2. Ingress API resource and its annotations.

Ingress has ingress controller specific annotations whereas service tries to provide ingress controller agnostic annotations. It is not recommended to mix annotations on service and ingress resources as those might conflict.

### Ingress Annotations on Services

Application services can be annotated for the platform to generate the required ingress routes. Use these annotations for any ingress controller type you choose.

```
kind: Deployment
apiVersion: apps/v1
metadata:
  name: whoami
  labels:
    app: whoami
spec:
  replicas: 2
  selector:
    matchLabels:
      app: whoami
  template:
    metadata:
      labels:
        app: whoami
    spec:
      containers:
        - name: whoami
          image: containous/whoami
          ports:
            - name: web
              containerPort: 80
---
apiVersion: v1
kind: Secret
metadata:
  name: whoami
type: kubernetes.io/tls
data:
  ca.crt: ...
  tls.crt: ...
  tls.key: ...
---
apiVersion: v1
kind: Service
metadata:
  name: whoami
  annotations:
    sherlock.nutanix.com/http-ingress-path: /notls
    sherlock.nutanix.com/https-ingress-path: /tls
    sherlock.nutanix.com/https-ingress-host: my-service.company.com
    sherlock.nutanix.com/https-ingress-secret: whoami
spec:
  ports:
    - protocol: TCP
      name: web
      port: 80
  selector:
    app: whoami
```

In the above example we used `sherlock.nutanix.com/http-ingress-path` annotation which exposed HTTP endpoint on any node IP. The app can be reached on `$NODE_IP:/notls` via HTTP or `my-service.company.com/tls` via HTTPS. External DNS must be configured for HTTP client to resolve domain name to set of node IPs.

Following annotations are supported on services:

* **sherlock.nutanix.com/http-ingress-path** - Exposes HTTP endpoint of service on given HTTP path. Defaults to `/`.

* **sherlock.nutanix.com/http-ingress-host** - Exposes HTTP endpoint of service on given virtual HTTP host. Ingress accepts traffic to all hosts if not specified.

* **sherlock.nutanix.com/https-ingress-path** - Exposes HTTP endpoint of service on given HTTP path using TLS/HTTPS for authentication and encryption. Defaults to `/`.

* **sherlock.nutanix.com/https-ingress-host** - Exposes HTTP endpoint of service using TLS/HTTPS leveraging SNI host names. Ingress accepts traffic to all hosts if not specified.

* **sherlock.nutanix.com/https-ingress-secret** - Exposes HTTP endpoint of service using TLS/HTTPS and provided certificate stored in Kubernetes secret. Certificate must be valid for chosen host.


### Ingress API Resource

Kubernetes has builtin support for an ingress API. See https://kubernetes.io/docs/concepts/services-networking/ingress

Traefik as well as ingress-nginx have their own annotations on ingress resources.

For Traefik see: https://docs.traefik.io/v1.7/configuration/backends/kubernetes/#annotations

Fon ingress-nginx refer to: https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/

Following is a sample app which exposes HTTP endpoint: 

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: whoami
  labels:
    app: whoami
spec:
  replicas: 1
  selector:
    matchLabels:
      app: whoami
  template:
    metadata:
      labels:
        app: whoami
    spec:
      containers:
        - name: whoami
          image: containous/whoami
          ports:
            - name: web
              containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: whoami
spec:
  ports:
    - protocol: TCP
      name: web
      port: 80
  selector:
    app: whoami
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: whoami
  labels:
    app: whoami
spec:
  rules:
    - http:
        paths:
        - path: /whoami
          backend:
            serviceName: whoami
            servicePort: web
```

## Access Services via Ingress

For the chosen ingress controller, both HTTP port 80 and HTTPS port 443 are open and listening for ingress traffic on all nodes in cluster. In case of Traefik port 8081 is open as well to give access to Traefik dashboard.