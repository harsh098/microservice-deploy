# Microservices Project : A Video Converter Service
This project was my first introduction to developing microservices and deploying them to a local **Kubernetes** cluster(**minikube**).  
Multiple repos were combined for your convinience.  

------

### Sub Repos for each service:-
1. **Main repo** [https://github.com/harsh098/microservice-deploy/](https://github.com/harsh098/microservice-deploy/)
2. **Authentication Service** [https://github.com/harsh098/microservice-deploy-auth](https://github.com/harsh098/microservice-deploy-auth)
3. **Gateway Service** [https://github.com/harsh098/microservice-deploy-gateway-svc](https://github.com/harsh098/microservice-deploy-gateway-svc)
4. **RabbitMQ deployment** [https://github.com/harsh098/microservice-deploy-rabbitmq](https://github.com/harsh098/microservice-deploy-rabbitmq)
5. **Converter Service** [https://github.com/harsh098/microservice-deploy-converter-service](https://github.com/harsh098/microservice-deploy-converter-service)
6. **Notification Service** [https://github.com/harsh098/microservice-deploy-notification-service](https://github.com/harsh098/microservice-deploy-notification-service)
------

### Setting up your Local kubernetes cluster


#### Part-I. Start Docker, mysqld, and mongod
Assuming you have `mysql` and `mongo` installed on local and `mongo` is configured to allow access without authentication.  

1. Configure You `mysqld.service` and `mongod.service` to allow all hosts i.e. `0.0.0.0` (for all IPv4) or `::` (for all IPv6 abd IPv4)  
 `sudo systemctl start docker mysqld and mongod`
2. Edit `init.sql` as instructed in the file
3. run `init.sql`
 

#### Part-II. Setting Up minikube and conatiners
1. Run the following commands
  ```
  minikube start
  eval $(minikube -p minikube docker-env)
  ``` 
2. Clone the git repo
3. cd into the directory  
   Run the following command ```./builder.py .```
4. edit following `secret.yaml` files for your setup 
   1. `JWT_SECRET` in `auth_service/manifests/secret.yaml [here](https://github.com/harsh098/microservice-deploy/blob/main/auth_service/manifests/secret.yaml)
   2. `GMAIL_ADDRESS` and `GMAIL_PASSWORD` in `notification_service/manifests/secret.yaml` [here](https://github.com/harsh098/microservice-deploy/blob/main/notification_service/manifests/secret.yaml)
5. Run `minikube ip`

####  Part-III. Edit your DNS Records

***Note:*** replace `192.168.49.2` with the **address** in the output of `minikube ip`  
Add the following lines to `/etc/hosts` (in **Mac/Linux**) or `C:\Windows\System32\Drivers\etc\hosts` (in **Windows**)  


```
  192.168.49.2   kubernetes.docker.internal
  192.168.49.2   vid2mp3.com
  192.168.49.2   rabbitmq-manager.com

```


#### Part-IV. Start the deployments
Run The following commands
1. cd into project directory  

```
kubectl create -f auth_service/manifests
kubectl create -f gateway/manifests
kubectl create -f rabbit/manifests
kubectl create -f converter_svc/manifests
kubectl create -f notification_service/manifests
```
2. **Mac and Windows Users need to run** `minikube tunnel` **in a separate terminal window**

## Running Demo

##### STEP-1 login via /login endpoint and get JWT
<img src="https://github.com/harsh098/microservice-deploy/blob/main/docs/images/login_endpoint.png?raw=true"/>

##### STEP-2 Upload video via /upload endpoint and validate using JWT
<img src="https://github.com/harsh098/microservice-deploy/blob/main/docs/images/secured_upload.png?raw=true"/>
<img src="https://github.com/harsh098/microservice-deploy/blob/main/docs/images/upload_body.png?raw=true"/>

##### STEP-3 The video is processed and notification received on e-mail
<img src="https://github.com/harsh098/microservice-deploy/blob/main/docs/images/email_from_notification_Service.png?raw=true"/>

##### STEP-4 Download the converted file using /download (validate using JWT)
<img src="https://github.com/harsh098/microservice-deploy/blob/main/docs/images/download_endpoint.png?raw=true"/>

##### Running Kubernetes cluster Objects

######   I. Pods
<img src="https://github.com/harsh098/microservice-deploy/blob/main/docs/images/pods_on_k8s.png?raw=true"/>  

######   II. Ingresses
<img src="https://github.com/harsh098/microservice-deploy/blob/main/docs/images/ingresses_on_k8s.png?raw=true"/>  

######   III. Deployments
<img src="https://github.com/harsh098/microservice-deploy/blob/main/docs/images/deployments_on_k8s.png?raw=true"/>  

######   IV.  Persistent Volumes
<img src="https://github.com/harsh098/microservice-deploy/blob/main/docs/images/pvc_k8s.png?raw=true"/>  

######   V. Stateful Sets
<img src="https://github.com/harsh098/microservice-deploy/blob/main/docs/images/statefulset.png?raw=true"/>

