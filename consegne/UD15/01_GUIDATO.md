# UD15 — Consegna laboratorio guidato

Partecipante: Stefano Raneri
Data e fuso orario: 09:46 CET
Repository operativo: Si

## Spiegazioni personali

Le prove dei comandi saranno aggiunte automaticamente dal guidato, nella parte successiva di questo file. Scrivi qui soltanto le brevi spiegazioni richieste:

- Come il selector del Service individua i Pod: Il Service cerca i Pod nello stesso namespace che hanno l'etichetta `app: web-intro`. Quando trova una corrispondenza esatta, registra i loro indirizzi IP negli EndpointSlice per mandargli il traffico.

- Che cosa cambia con lo scaling e perché la revisione resta uguale: Con lo scaling cambia solo quante copie del Pod devono girare (da 1 a 3). La revisione non aumenta perché non abbiamo modificato le impostazioni del container o del template, ma solo il numero di repliche.

- Confronto fra immagine aggiornata e immagine dopo il rollback: Con l'aggiornamento i Pod usavano la versione nuova `nginx:1.29.0-alpine`. Dopo il comando di rollback Kubernetes ha spento quei Pod e ne ha creati di nuovi tornando alla versione di partenza `nginx:1.28.0-alpine`.

- Causa del guasto letta negli eventi e disponibilità dei log: Negli eventi l'errore `ErrImagePull` e `ImagePullBackOff` segnala che il tag `tag-ft152-che-non-esiste` non è stato trovato su Docker Hub. I comandi `logs` e `--previous` non mostrano nulla perché il container non è mai stato scaricato e quindi non è mai partito.

- Esiti osservati nel browser per immagine iniziale, aggiornata e dopo rollback: In tutti e tre i casi il browser ha aperto regolarmente la pagina di benvenuto "Welcome to nginx!", restituendo codice HTTP 200 via porta 8081. A vista la pagina era sempre uguale, ma la versione reale cambiava nei dettagli del Pod.

- Tempi effettivi e problemi incontrati: Il laboratorio ha richiesto circa 40 minuti. All'inizio il nodo ha impiegato qualche istante a diventare pronto per un avviso di taint e il pull della prima immagine ha richiesto pochi secondi di attesa.

- Profilo che intendo conservare attivo/fermo a fine giornata: Mantengo il profilo `minikube` attivo (Running) per proseguire subito con le attività del laboratorio autonomo.

- Risorse Azure precedenti eventualmente ancora conservate: Nessuna risorsa attiva su Azure, l'esercitazione si è svolta interamente in locale su Minikube.

## Evidenze raccolte dal terminale

I blocchi del guidato aggiungono qui data/ora e output effettivi. Gli errori restano visibili insieme alla successiva prova corretta. Non sostituire un errore con un risultato atteso.

### Verifica profilo `minikube` e contesto con `kubectl`

```bash
$ minikube status -p minikube
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

```bash
$ kubectl config get-contexts
CURRENT   NAME       CLUSTER    AUTHINFO   NAMESPACE
*         minikube   minikube   minikube   default
```

```bash
$ kubectl --context=minikube version
Client Version: v1.37.2
Kustomize Version: v5.8.1
Server Version: v1.37.0
```

```bash
$ kubectl --context=minikube cluster-info
Kubernetes control plane is running at https://127.0.0.1:45879
CoreDNS is running at https://127.0.0.1:45879/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

```bash
$ kubectl --context=minikube get nodes -o wide
NAME       STATUS     ROLES           AGE    VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION                   CONTAINER-RUNTIME
minikube   NotReady   control-plane   5m8s   v1.37.0   192.168.49.2   <none>        Debian GNU/Linux 12 (bookworm)   7.0.14-201.fc44.x86_64 (amd64)   containerd://2.3.4
```

```bash
$ kubectl --context=minikube get pods -n kube-system
NAME                               READY   STATUS             RESTARTS       AGE
coredns-559f6c778d-pzhzl           0/1     Pending            0              5m2s
etcd-minikube                      1/1     Running            0              5m9s
kindnet-ts9nz                      1/1     Running            0              5m2s
kube-apiserver-minikube            1/1     Running            0              5m10s
kube-controller-manager-minikube   1/1     Running            0              5m9s
kube-proxy-wwsgr                   0/1     CrashLoopBackOff   5 (2m4s ago)   5m2s
kube-scheduler-minikube            1/1     Running            0              5m10s
storage-provisioner                0/1     Pending            0              5m7s
```

```bash
$ minikube -p minikube ssh -- "curl --max-time 15 -sS -o /dev/null -w 'MINIKUBE HTTP %{http_code}\n' https://registry-1.docker.io/v2/"
MINIKUBE HTTP 401
```

### Primo Deployment e collegamento ai Pod

```text
2026-11-04T10:11:27+01:00
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES                SELECTOR
deployment.apps/web-intro   1/1     1            1           8m59s   web          nginx:1.28.0-alpine   app=web-intro

NAME                                   DESIRED   CURRENT   READY   AGE     CONTAINERS   IMAGES                SELECTOR
replicaset.apps/web-intro-846844b5c9   1         1         1       8m59s   web          nginx:1.28.0-alpine   app=web-intro,pod-template-hash=846844b5c9

NAME                             READY   STATUS    RESTARTS   AGE     IP           NODE       NOMINATED NODE   READINESS GATES
pod/web-intro-846844b5c9-22cgf   1/1     Running   0          8m59s   10.244.0.2   minikube   <none>           <none>
NAME                         READY   STATUS    RESTARTS   AGE     LABELS
web-intro-846844b5c9-22cgf   1/1     Running   0          8m59s   app=web-intro,pod-template-hash=846844b5c9
Name:                   web-intro
Namespace:              ft152-ud15
CreationTimestamp:      Wed, 04 Nov 2026 10:02:28 +0100
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=web-intro
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=web-intro
  Containers:
   web:
    Image:         nginx:1.28.0-alpine
    Port:          80/TCP (http)
    Host Port:     0/TCP (http)
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   web-intro-846844b5c9 (1/1 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  8m59s  deployment-controller  Scaled up replica set web-intro-846844b5c9 from 0 to 1
LAST SEEN   TYPE      REASON              OBJECT                            MESSAGE
3m31s       Warning   FailedScheduling    pod/web-intro-846844b5c9-22cgf    0/1 nodes are available: 1 node(s) had untolerated taint(s). preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
8m59s       Normal    SuccessfulCreate    replicaset/web-intro-846844b5c9   Created pod: web-intro-846844b5c9-22cgf
8m59s       Normal    ScalingReplicaSet   deployment/web-intro              Scaled up replica set web-intro-846844b5c9 from 0 to 1
104s        Normal    Scheduled           pod/web-intro-846844b5c9-22cgf    Successfully assigned ft152-ud15/web-intro-846844b5c9-22cgf to minikube
103s        Normal    Pulling             pod/web-intro-846844b5c9-22cgf    Pulling image "nginx:1.28.0-alpine"
95s         Normal    Pulled              pod/web-intro-846844b5c9-22cgf    Successfully pulled image "nginx:1.28.0-alpine" in 7.892s (7.892s including waiting). Image size: 21015643 bytes.
95s         Normal    Created             pod/web-intro-846844b5c9-22cgf    Container created
95s         Normal    Started             pod/web-intro-846844b5c9-22cgf    Container started
```

### Service web-intro e indirizzi dei Pod

```text
2026-11-04T10:15:37+01:00
Name:                     web-intro
Namespace:                ft152-ud15
Labels:                   <none>
Annotations:              <none>
Selector:                 app=web-intro
Type:                     ClusterIP
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.98.208.71
IPs:                      10.98.208.71
Port:                     http  80/TCP
TargetPort:               http/TCP
Endpoints:                10.244.0.2:80
Session Affinity:         None
Internal Traffic Policy:  Cluster
Events:                   <none>
NAME                         READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
web-intro-846844b5c9-22cgf   1/1     Running   0          13m   10.244.0.2   minikube   <none>           <none>
apiVersion: v1
items:
- addressType: IPv4
  apiVersion: discovery.k8s.io/v1
  endpoints:
  - addresses:
    - 10.244.0.2
    conditions:
      ready: true
      serving: true
      terminating: false
    nodeName: minikube
    targetRef:
      kind: Pod
      name: web-intro-846844b5c9-22cgf
      namespace: ft152-ud15
      uid: fd3fe2d8-4ba5-4992-9733-c379dc5e5798
  kind: EndpointSlice
  metadata:
    annotations:
      endpoints.kubernetes.io/last-change-trigger-time: "2026-11-04T09:15:05Z"
    creationTimestamp: "2026-11-04T09:15:05Z"
    generateName: web-intro-
    generation: 1
    labels:
      endpointslice.kubernetes.io/managed-by: endpointslice-controller.k8s.io
      kubernetes.io/service-name: web-intro
    name: web-intro-zxhbp
    namespace: ft152-ud15
    ownerReferences:
    - apiVersion: v1
      blockOwnerDeletion: true
      controller: true
      kind: Service
      name: web-intro
      uid: e2b59c3c-6fdf-488e-8c85-9def21deb4b7
    resourceVersion: "1454"
    uid: 3d7572ea-2acc-4dad-8464-065c21ebfc16
  ports:
  - name: http
    port: 80
    protocol: TCP
kind: List
metadata:
  resourceVersion: ""
```

### Risposta HTTP della demo iniziale

```text
2026-11-04T10:16:01+01:00
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed

  0      0   0      0   0      0      0      0                              0
100    615 100    615   0      0  67858      0                              0
100    615 100    615   0      0  66949      0                              0
100    615 100    615   0      0  66050      0                              0
HTTP/1.1 200 OK
Server: nginx/1.28.0
Date: Wed, 04 Nov 2026 09:16:02 GMT
Content-Type: text/html
Content-Length: 615
Last-Modified: Wed, 23 Apr 2025 12:59:25 GMT
Connection: keep-alive
ETag: "6808e42d-267"
Accept-Ranges: bytes

<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

### Prima dello scaling: una replica e revisione corrente

```text
2026-11-04T10:18:53+01:00
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                SELECTOR
deployment.apps/web-intro   1/1     1            1           16m   web          nginx:1.28.0-alpine   app=web-intro

NAME                                   DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES                SELECTOR
replicaset.apps/web-intro-846844b5c9   1         1         1       16m   web          nginx:1.28.0-alpine   app=web-intro,pod-template-hash=846844b5c9

NAME                             READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
pod/web-intro-846844b5c9-22cgf   1/1     Running   0          16m   10.244.0.2   minikube   <none>           <none>
deployment.apps/web-intro
REVISION  CHANGE-CAUSE
1         <none>

```

### Dopo lo scaling: tre Pod Nginx

```text
2026-11-04T10:19:10+01:00
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                SELECTOR
deployment.apps/web-intro   3/3     3            3           16m   web          nginx:1.28.0-alpine   app=web-intro

NAME                                   DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES                SELECTOR
replicaset.apps/web-intro-846844b5c9   3         3         3       16m   web          nginx:1.28.0-alpine   app=web-intro,pod-template-hash=846844b5c9

NAME                             READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
pod/web-intro-846844b5c9-22cgf   1/1     Running   0          16m   10.244.0.2   minikube   <none>           <none>
pod/web-intro-846844b5c9-cxqdg   1/1     Running   0          9s    10.244.0.5   minikube   <none>           <none>
pod/web-intro-846844b5c9-qtwfm   1/1     Running   0          9s    10.244.0.4   minikube   <none>           <none>
apiVersion: v1
items:
- addressType: IPv4
  apiVersion: discovery.k8s.io/v1
  endpoints:
  - addresses:
    - 10.244.0.2
    conditions:
      ready: true
      serving: true
      terminating: false
    nodeName: minikube
    targetRef:
      kind: Pod
      name: web-intro-846844b5c9-22cgf
      namespace: ft152-ud15
      uid: fd3fe2d8-4ba5-4992-9733-c379dc5e5798
  - addresses:
    - 10.244.0.4
    conditions:
      ready: true
      serving: true
      terminating: false
    nodeName: minikube
    targetRef:
      kind: Pod
      name: web-intro-846844b5c9-qtwfm
      namespace: ft152-ud15
      uid: fca7b4a0-1b10-4c67-83f7-38ef4d5aef07
  - addresses:
    - 10.244.0.5
    conditions:
      ready: true
      serving: true
      terminating: false
    nodeName: minikube
    targetRef:
      kind: Pod
      name: web-intro-846844b5c9-cxqdg
      namespace: ft152-ud15
      uid: 3d324fe8-f60e-42a0-b461-bb31337c8388
  kind: EndpointSlice
  metadata:
    annotations:
      endpoints.kubernetes.io/last-change-trigger-time: "2026-11-04T09:19:02Z"
    creationTimestamp: "2026-11-04T09:15:05Z"
    generateName: web-intro-
    generation: 3
    labels:
      endpointslice.kubernetes.io/managed-by: endpointslice-controller.k8s.io
      kubernetes.io/service-name: web-intro
    name: web-intro-zxhbp
    namespace: ft152-ud15
    ownerReferences:
    - apiVersion: v1
      blockOwnerDeletion: true
      controller: true
      kind: Service
      name: web-intro
      uid: e2b59c3c-6fdf-488e-8c85-9def21deb4b7
    resourceVersion: "1702"
    uid: 3d7572ea-2acc-4dad-8464-065c21ebfc16
  ports:
  - name: http
    port: 80
    protocol: TCP
kind: List
metadata:
  resourceVersion: ""
deployment.apps/web-intro
REVISION  CHANGE-CAUSE
1         <none>

```

### File riallineato a tre repliche

```text
2026-11-04T10:19:39+01:00
# Micro-demo: Nginx standard, non il frontend completo del Catalogo.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-intro
  namespace: ft152-ud15
spec:
  replicas: 3
  # Conserviamo i template precedenti per l'esercizio di rollback.
  revisionHistoryLimit: 5
  selector:
    matchLabels:
      app: web-intro
  template:
    metadata:
      labels:
        app: web-intro
    spec:
      containers:
        - name: web
          image: nginx:1.28.0-alpine
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 80
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
web-intro   3/3     3            3           17m
```

### Prima dell’aggiornamento immagine

```text
2026-11-04T10:20:01+01:00
deployment.apps/web-intro
REVISION  CHANGE-CAUSE
1         <none>

apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "1"
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"name":"web-intro","namespace":"ft152-ud15"},"spec":{"replicas":3,"revisionHistoryLimit":5,"selector":{"matchLabels":{"app":"web-intro"}},"template":{"metadata":{"labels":{"app":"web-intro"}},"spec":{"containers":[{"image":"nginx:1.28.0-alpine","imagePullPolicy":"IfNotPresent","name":"web","ports":[{"containerPort":80,"name":"http"}]}]}}}}
  creationTimestamp: "2026-11-04T09:02:28Z"
  generation: 3
  name: web-intro
  namespace: ft152-ud15
  resourceVersion: "1734"
  uid: 2f1431ab-3a7f-4cc2-87ca-4f4b6164cfcf
spec:
  progressDeadlineSeconds: 600
  replicas: 3
  revisionHistoryLimit: 5
  selector:
    matchLabels:
      app: web-intro
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: web-intro
    spec:
      containers:
      - image: nginx:1.28.0-alpine
        imagePullPolicy: IfNotPresent
        name: web
        ports:
        - containerPort: 80
          name: http
          protocol: TCP
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
  availableReplicas: 3
  conditions:
  - lastTransitionTime: "2026-11-04T09:02:28Z"
    lastUpdateTime: "2026-11-04T09:09:52Z"
    message: ReplicaSet "web-intro-846844b5c9" has successfully progressed.
    reason: NewReplicaSetAvailable
    status: "True"
    type: Progressing
  - lastTransitionTime: "2026-11-04T09:19:02Z"
    lastUpdateTime: "2026-11-04T09:19:02Z"
    message: Deployment has minimum availability.
    reason: MinimumReplicasAvailable
    status: "True"
    type: Available
  observedGeneration: 3
  readyReplicas: 3
  replicas: 3
  terminatingReplicas: 0
  updatedReplicas: 3
```

### Immagine aggiornata e Pod avviati

```text
2026-11-04T10:20:32+01:00
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                SELECTOR
deployment.apps/web-intro   3/3     3            3           18m   web          nginx:1.29.0-alpine   app=web-intro

NAME                                   DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES                SELECTOR
replicaset.apps/web-intro-54449bc466   3         3         3       24s   web          nginx:1.29.0-alpine   app=web-intro,pod-template-hash=54449bc466
replicaset.apps/web-intro-846844b5c9   0         0         0       18m   web          nginx:1.28.0-alpine   app=web-intro,pod-template-hash=846844b5c9

NAME                             READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
pod/web-intro-54449bc466-lbfqx   1/1     Running   0          16s   10.244.0.7   minikube   <none>           <none>
pod/web-intro-54449bc466-vhrvv   1/1     Running   0          15s   10.244.0.8   minikube   <none>           <none>
pod/web-intro-54449bc466-zmr2z   1/1     Running   0          24s   10.244.0.6   minikube   <none>           <none>
apiVersion: v1
items:
- apiVersion: v1
  kind: Pod
  metadata:
    creationTimestamp: "2026-11-04T09:20:16Z"
    generateName: web-intro-54449bc466-
    generation: 1
    labels:
      app: web-intro
      pod-template-hash: 54449bc466
    name: web-intro-54449bc466-lbfqx
    namespace: ft152-ud15
    ownerReferences:
    - apiVersion: apps/v1
      blockOwnerDeletion: true
      controller: true
      kind: ReplicaSet
      name: web-intro-54449bc466
      uid: d4585535-75c0-4196-9115-23580f09f09b
    resourceVersion: "1827"
    uid: 0a9544c1-d0bc-4f2a-9270-67f0f991dd3b
  spec:
    containers:
    - image: nginx:1.29.0-alpine
      imagePullPolicy: IfNotPresent
      name: web
      ports:
      - containerPort: 80
        name: http
        protocol: TCP
      resources: {}
      terminationMessagePath: /dev/termination-log
      terminationMessagePolicy: File
      volumeMounts:
      - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
        name: kube-api-access-trvjk
        readOnly: true
    dnsPolicy: ClusterFirst
    enableServiceLinks: true
    nodeName: minikube
    preemptionPolicy: PreemptLowerPriority
    priority: 0
    restartPolicy: Always
    schedulerName: default-scheduler
    securityContext: {}
    serviceAccount: default
    serviceAccountName: default
    terminationGracePeriodSeconds: 30
    tolerations:
    - effect: NoExecute
      key: node.kubernetes.io/not-ready
      operator: Exists
      tolerationSeconds: 300
    - effect: NoExecute
      key: node.kubernetes.io/unreachable
      operator: Exists
      tolerationSeconds: 300
    volumes:
    - name: kube-api-access-trvjk
      projected:
        defaultMode: 420
        sources:
        - serviceAccountToken:
            expirationSeconds: 3607
            path: token
        - configMap:
            items:
            - key: ca.crt
              path: ca.crt
            name: kube-root-ca.crt
        - downwardAPI:
            items:
            - fieldRef:
                apiVersion: v1
                fieldPath: metadata.namespace
              path: namespace
  status:
    conditions:
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:17Z"
      observedGeneration: 1
      status: "True"
      type: PodReadyToStartContainers
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:16Z"
      observedGeneration: 1
      status: "True"
      type: Initialized
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:17Z"
      observedGeneration: 1
      status: "True"
      type: Ready
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:17Z"
      observedGeneration: 1
      status: "True"
      type: ContainersReady
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:16Z"
      observedGeneration: 1
      status: "True"
      type: PodScheduled
    containerStatuses:
    - containerID: containerd://734879acdd9064849254c915a70306a1182fa3e3a4d6484c9ad8c12034e54228
      image: docker.io/library/nginx:1.29.0-alpine
      imageID: docker.io/library/nginx@sha256:d67ea0d64d518b1bb04acde3b00f722ac3e9764b3209a9b0a98924ba35e4b779
      lastState: {}
      name: web
      ready: true
      resources: {}
      restartCount: 0
      started: true
      state:
        running:
          startedAt: "2026-11-04T09:20:17Z"
      user:
        linux:
          gid: 0
          supplementalGroups:
          - 0
          - 1
          - 2
          - 3
          - 4
          - 6
          - 10
          - 11
          - 20
          - 26
          - 27
          uid: 0
      volumeMounts:
      - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
        name: kube-api-access-trvjk
        readOnly: true
        recursiveReadOnly: Disabled
    hostIP: 192.168.49.2
    hostIPs:
    - ip: 192.168.49.2
    observedGeneration: 1
    phase: Running
    podIP: 10.244.0.7
    podIPs:
    - ip: 10.244.0.7
    qosClass: BestEffort
    resources: {}
    startTime: "2026-11-04T09:20:16Z"
- apiVersion: v1
  kind: Pod
  metadata:
    creationTimestamp: "2026-11-04T09:20:17Z"
    generateName: web-intro-54449bc466-
    generation: 1
    labels:
      app: web-intro
      pod-template-hash: 54449bc466
    name: web-intro-54449bc466-vhrvv
    namespace: ft152-ud15
    ownerReferences:
    - apiVersion: apps/v1
      blockOwnerDeletion: true
      controller: true
      kind: ReplicaSet
      name: web-intro-54449bc466
      uid: d4585535-75c0-4196-9115-23580f09f09b
    resourceVersion: "1864"
    uid: d81a0881-a6d7-4451-95ef-943e8d6ee118
  spec:
    containers:
    - image: nginx:1.29.0-alpine
      imagePullPolicy: IfNotPresent
      name: web
      ports:
      - containerPort: 80
        name: http
        protocol: TCP
      resources: {}
      terminationMessagePath: /dev/termination-log
      terminationMessagePolicy: File
      volumeMounts:
      - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
        name: kube-api-access-z5rwq
        readOnly: true
    dnsPolicy: ClusterFirst
    enableServiceLinks: true
    nodeName: minikube
    preemptionPolicy: PreemptLowerPriority
    priority: 0
    restartPolicy: Always
    schedulerName: default-scheduler
    securityContext: {}
    serviceAccount: default
    serviceAccountName: default
    terminationGracePeriodSeconds: 30
    tolerations:
    - effect: NoExecute
      key: node.kubernetes.io/not-ready
      operator: Exists
      tolerationSeconds: 300
    - effect: NoExecute
      key: node.kubernetes.io/unreachable
      operator: Exists
      tolerationSeconds: 300
    volumes:
    - name: kube-api-access-z5rwq
      projected:
        defaultMode: 420
        sources:
        - serviceAccountToken:
            expirationSeconds: 3607
            path: token
        - configMap:
            items:
            - key: ca.crt
              path: ca.crt
            name: kube-root-ca.crt
        - downwardAPI:
            items:
            - fieldRef:
                apiVersion: v1
                fieldPath: metadata.namespace
              path: namespace
  status:
    conditions:
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:17Z"
      observedGeneration: 1
      status: "True"
      type: PodReadyToStartContainers
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:17Z"
      observedGeneration: 1
      status: "True"
      type: Initialized
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:18Z"
      observedGeneration: 1
      status: "True"
      type: Ready
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:18Z"
      observedGeneration: 1
      status: "True"
      type: ContainersReady
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:17Z"
      observedGeneration: 1
      status: "True"
      type: PodScheduled
    containerStatuses:
    - containerID: containerd://ee26116cbea6bc51aef5461d32295d1241d27ed6bbb89c05342cfcbba446c9d9
      image: docker.io/library/nginx:1.29.0-alpine
      imageID: docker.io/library/nginx@sha256:d67ea0d64d518b1bb04acde3b00f722ac3e9764b3209a9b0a98924ba35e4b779
      lastState: {}
      name: web
      ready: true
      resources: {}
      restartCount: 0
      started: true
      state:
        running:
          startedAt: "2026-11-04T09:20:18Z"
      user:
        linux:
          gid: 0
          supplementalGroups:
          - 0
          - 1
          - 2
          - 3
          - 4
          - 6
          - 10
          - 11
          - 20
          - 26
          - 27
          uid: 0
      volumeMounts:
      - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
        name: kube-api-access-z5rwq
        readOnly: true
        recursiveReadOnly: Disabled
    hostIP: 192.168.49.2
    hostIPs:
    - ip: 192.168.49.2
    observedGeneration: 1
    phase: Running
    podIP: 10.244.0.8
    podIPs:
    - ip: 10.244.0.8
    qosClass: BestEffort
    resources: {}
    startTime: "2026-11-04T09:20:17Z"
- apiVersion: v1
  kind: Pod
  metadata:
    creationTimestamp: "2026-11-04T09:20:08Z"
    generateName: web-intro-54449bc466-
    generation: 1
    labels:
      app: web-intro
      pod-template-hash: 54449bc466
    name: web-intro-54449bc466-zmr2z
    namespace: ft152-ud15
    ownerReferences:
    - apiVersion: apps/v1
      blockOwnerDeletion: true
      controller: true
      kind: ReplicaSet
      name: web-intro-54449bc466
      uid: d4585535-75c0-4196-9115-23580f09f09b
    resourceVersion: "1792"
    uid: bfc55ef4-9f3f-471e-b32a-20607fbc29cf
  spec:
    containers:
    - image: nginx:1.29.0-alpine
      imagePullPolicy: IfNotPresent
      name: web
      ports:
      - containerPort: 80
        name: http
        protocol: TCP
      resources: {}
      terminationMessagePath: /dev/termination-log
      terminationMessagePolicy: File
      volumeMounts:
      - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
        name: kube-api-access-fv8b5
        readOnly: true
    dnsPolicy: ClusterFirst
    enableServiceLinks: true
    nodeName: minikube
    preemptionPolicy: PreemptLowerPriority
    priority: 0
    restartPolicy: Always
    schedulerName: default-scheduler
    securityContext: {}
    serviceAccount: default
    serviceAccountName: default
    terminationGracePeriodSeconds: 30
    tolerations:
    - effect: NoExecute
      key: node.kubernetes.io/not-ready
      operator: Exists
      tolerationSeconds: 300
    - effect: NoExecute
      key: node.kubernetes.io/unreachable
      operator: Exists
      tolerationSeconds: 300
    volumes:
    - name: kube-api-access-fv8b5
      projected:
        defaultMode: 420
        sources:
        - serviceAccountToken:
            expirationSeconds: 3607
            path: token
        - configMap:
            items:
            - key: ca.crt
              path: ca.crt
            name: kube-root-ca.crt
        - downwardAPI:
            items:
            - fieldRef:
                apiVersion: v1
                fieldPath: metadata.namespace
              path: namespace
  status:
    conditions:
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:08Z"
      observedGeneration: 1
      status: "True"
      type: PodReadyToStartContainers
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:08Z"
      observedGeneration: 1
      status: "True"
      type: Initialized
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:16Z"
      observedGeneration: 1
      status: "True"
      type: Ready
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:16Z"
      observedGeneration: 1
      status: "True"
      type: ContainersReady
    - lastProbeTime: null
      lastTransitionTime: "2026-11-04T09:20:08Z"
      observedGeneration: 1
      status: "True"
      type: PodScheduled
    containerStatuses:
    - containerID: containerd://84e8078e24272f317199c2b97d6f328355237ba520ca2e04a353bffc04d9181b
      image: docker.io/library/nginx:1.29.0-alpine
      imageID: docker.io/library/nginx@sha256:d67ea0d64d518b1bb04acde3b00f722ac3e9764b3209a9b0a98924ba35e4b779
      lastState: {}
      name: web
      ready: true
      resources: {}
      restartCount: 0
      started: true
      state:
        running:
          startedAt: "2026-11-04T09:20:16Z"
      user:
        linux:
          gid: 0
          supplementalGroups:
          - 0
          - 1
          - 2
          - 3
          - 4
          - 6
          - 10
          - 11
          - 20
          - 26
          - 27
          uid: 0
      volumeMounts:
      - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
        name: kube-api-access-fv8b5
        readOnly: true
        recursiveReadOnly: Disabled
    hostIP: 192.168.49.2
    hostIPs:
    - ip: 192.168.49.2
    observedGeneration: 1
    phase: Running
    podIP: 10.244.0.6
    podIPs:
    - ip: 10.244.0.6
    qosClass: BestEffort
    resources: {}
    startTime: "2026-11-04T09:20:08Z"
kind: List
metadata:
  resourceVersion: ""
deployment.apps/web-intro
REVISION  CHANGE-CAUSE
1         <none>
2         <none>

```

### Test HTTP dopo aggiornamento immagine

```text
2026-11-04T10:22:38+01:00
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed

  0      0   0      0   0      0      0      0                              0
100    615 100    615   0      0  65376      0                              0
100    615 100    615   0      0  64832      0                              0
100    615 100    615   0      0  64310      0                              0
HTTP/1.1 200 OK
Server: nginx/1.29.0
Date: Wed, 04 Nov 2026 09:22:38 GMT
Content-Type: text/html
Content-Length: 615
Last-Modified: Tue, 24 Jun 2025 17:57:38 GMT
Connection: keep-alive
ETag: "685ae712-267"
Accept-Ranges: bytes

<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

### Dopo il rollback dell’immagine

```text
2026-11-04T10:24:13+01:00
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                SELECTOR
deployment.apps/web-intro   3/3     3            3           21m   web          nginx:1.28.0-alpine   app=web-intro

NAME                                   DESIRED   CURRENT   READY   AGE    CONTAINERS   IMAGES                SELECTOR
replicaset.apps/web-intro-54449bc466   0         0         0       4m5s   web          nginx:1.29.0-alpine   app=web-intro,pod-template-hash=54449bc466
replicaset.apps/web-intro-846844b5c9   3         3         3       21m    web          nginx:1.28.0-alpine   app=web-intro,pod-template-hash=846844b5c9

NAME                             READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
pod/web-intro-846844b5c9-4q8ks   1/1     Running   0          72s   10.244.0.11   minikube   <none>           <none>
pod/web-intro-846844b5c9-x6njk   1/1     Running   0          74s   10.244.0.9    minikube   <none>           <none>
pod/web-intro-846844b5c9-zskv9   1/1     Running   0          73s   10.244.0.10   minikube   <none>           <none>
deployment.apps/web-intro
REVISION  CHANGE-CAUSE
2         <none>
3         <none>

```

### Guasto di immagine: stato e messaggio osservati

```text
2026-11-04T10:26:20+01:00
NAME                         READY   STATUS             RESTARTS   AGE     IP            NODE       NOMINATED NODE   READINESS GATES
web-intro-6d4c975bcd-4929s   0/1     ImagePullBackOff   0          77s     10.244.0.12   minikube   <none>           <none>
web-intro-846844b5c9-4q8ks   1/1     Running            0          3m19s   10.244.0.11   minikube   <none>           <none>
web-intro-846844b5c9-x6njk   1/1     Running            0          3m21s   10.244.0.9    minikube   <none>           <none>
web-intro-846844b5c9-zskv9   1/1     Running            0          3m20s   10.244.0.10   minikube   <none>           <none>
Name:             web-intro-6d4c975bcd-4929s
Namespace:        ft152-ud15
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Wed, 04 Nov 2026 10:25:03 +0100
Labels:           app=web-intro
                  pod-template-hash=6d4c975bcd
Annotations:      <none>
Status:           Pending
IP:               10.244.0.12
IPs:
  IP:           10.244.0.12
Controlled By:  ReplicaSet/web-intro-6d4c975bcd
Containers:
  web:
    Container ID:
    Image:          nginx:tag-ft152-che-non-esiste
    Image ID:
    Port:           80/TCP (http)
    Host Port:      0/TCP (http)
    State:          Waiting
      Reason:       ImagePullBackOff
    Ready:          False
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-tsmzj (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       False
  ContainersReady             False
  PodScheduled                True
Volumes:
  kube-api-access-tsmzj:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    Optional:                false
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  77s                default-scheduler  Successfully assigned ft152-ud15/web-intro-6d4c975bcd-4929s to minikube
  Normal   Pulling    37s (x3 over 76s)  kubelet            spec.containers{web}: Pulling image "nginx:tag-ft152-che-non-esiste"
  Warning  Failed     36s (x3 over 75s)  kubelet            spec.containers{web}: Failed to pull image "nginx:tag-ft152-che-non-esiste": rpc error: code = NotFound desc = failed to pull and unpack image "docker.io/library/nginx:tag-ft152-che-non-esiste": failed to resolve reference "docker.io/library/nginx:tag-ft152-che-non-esiste": docker.io/library/nginx:tag-ft152-che-non-esiste: not found
  Warning  Failed     36s (x3 over 75s)  kubelet            spec.containers{web}: Error: ErrImagePull
  Normal   BackOff    10s (x4 over 75s)  kubelet            spec.containers{web}: Back-off pulling image "nginx:tag-ft152-che-non-esiste"
  Warning  Failed     10s (x4 over 75s)  kubelet            spec.containers{web}: Error: ImagePullBackOff
LAST SEEN   TYPE      REASON              OBJECT                            MESSAGE
3m21s       Normal    ScalingReplicaSet   deployment/web-intro              Scaled up replica set web-intro-846844b5c9 from 0 to 1
18m         Warning   FailedScheduling    pod/web-intro-846844b5c9-22cgf    0/1 nodes are available: 1 node(s) had untolerated taint(s). preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
23m         Normal    SuccessfulCreate    replicaset/web-intro-846844b5c9   Created pod: web-intro-846844b5c9-22cgf
16m         Normal    Scheduled           pod/web-intro-846844b5c9-22cgf    Successfully assigned ft152-ud15/web-intro-846844b5c9-22cgf to minikube
16m         Normal    Pulling             pod/web-intro-846844b5c9-22cgf    Pulling image "nginx:1.28.0-alpine"
16m         Normal    Started             pod/web-intro-846844b5c9-22cgf    Container started
16m         Normal    Pulled              pod/web-intro-846844b5c9-22cgf    Successfully pulled image "nginx:1.28.0-alpine" in 7.892s (7.892s including waiting). Image size: 21015643 bytes.
16m         Normal    Created             pod/web-intro-846844b5c9-22cgf    Container created
7m19s       Normal    Pulled              pod/web-intro-846844b5c9-qtwfm    Container image "nginx:1.28.0-alpine" already present on machine and can be accessed by the pod
7m19s       Normal    Scheduled           pod/web-intro-846844b5c9-cxqdg    Successfully assigned ft152-ud15/web-intro-846844b5c9-cxqdg to minikube
7m19s       Normal    Pulled              pod/web-intro-846844b5c9-cxqdg    Container image "nginx:1.28.0-alpine" already present on machine and can be accessed by the pod
7m19s       Normal    Scheduled           pod/web-intro-846844b5c9-qtwfm    Successfully assigned ft152-ud15/web-intro-846844b5c9-qtwfm to minikube
7m19s       Normal    ScalingReplicaSet   deployment/web-intro              Scaled up replica set web-intro-846844b5c9 from 1 to 3
7m19s       Normal    Created             pod/web-intro-846844b5c9-qtwfm    Container created
7m19s       Normal    SuccessfulCreate    replicaset/web-intro-846844b5c9   Created pod: web-intro-846844b5c9-cxqdg
7m19s       Normal    SuccessfulCreate    replicaset/web-intro-846844b5c9   Created pod: web-intro-846844b5c9-qtwfm
7m18s       Normal    Created             pod/web-intro-846844b5c9-cxqdg    Container created
7m18s       Normal    Started             pod/web-intro-846844b5c9-qtwfm    Container started
7m18s       Normal    Started             pod/web-intro-846844b5c9-cxqdg    Container started
6m12s       Normal    ScalingReplicaSet   deployment/web-intro              Scaled up replica set web-intro-54449bc466 from 0 to 1
6m12s       Normal    Scheduled           pod/web-intro-54449bc466-zmr2z    Successfully assigned ft152-ud15/web-intro-54449bc466-zmr2z to minikube
6m12s       Normal    Pulling             pod/web-intro-54449bc466-zmr2z    Pulling image "nginx:1.29.0-alpine"
6m12s       Normal    SuccessfulCreate    replicaset/web-intro-54449bc466   Created pod: web-intro-54449bc466-zmr2z
6m4s        Normal    Started             pod/web-intro-54449bc466-zmr2z    Container started
6m4s        Normal    Scheduled           pod/web-intro-54449bc466-lbfqx    Successfully assigned ft152-ud15/web-intro-54449bc466-lbfqx to minikube
6m4s        Normal    ScalingReplicaSet   deployment/web-intro              Scaled up replica set web-intro-54449bc466 from 1 to 2
6m4s        Normal    SuccessfulDelete    replicaset/web-intro-846844b5c9   Deleted pod: web-intro-846844b5c9-qtwfm
6m4s        Normal    SuccessfulCreate    replicaset/web-intro-54449bc466   Created pod: web-intro-54449bc466-lbfqx
6m4s        Normal    Killing             pod/web-intro-846844b5c9-qtwfm    Stopping container web
6m4s        Normal    ScalingReplicaSet   deployment/web-intro              Scaled down replica set web-intro-846844b5c9 from 3 to 2
6m4s        Normal    Created             pod/web-intro-54449bc466-zmr2z    Container created
6m4s        Normal    Pulled              pod/web-intro-54449bc466-zmr2z    Successfully pulled image "nginx:1.29.0-alpine" in 7.263s (7.263s including waiting). Image size: 22414794 bytes.
6m3s        Normal    ScalingReplicaSet   deployment/web-intro              Scaled up replica set web-intro-54449bc466 from 2 to 3
6m3s        Normal    Pulled              pod/web-intro-54449bc466-lbfqx    Container image "nginx:1.29.0-alpine" already present on machine and can be accessed by the pod
6m3s        Normal    SuccessfulCreate    replicaset/web-intro-54449bc466   Created pod: web-intro-54449bc466-vhrvv
6m3s        Normal    Started             pod/web-intro-54449bc466-lbfqx    Container started
6m3s        Normal    Scheduled           pod/web-intro-54449bc466-vhrvv    Successfully assigned ft152-ud15/web-intro-54449bc466-vhrvv to minikube
6m3s        Normal    Created             pod/web-intro-54449bc466-lbfqx    Container created
6m3s        Normal    SuccessfulDelete    replicaset/web-intro-846844b5c9   Deleted pod: web-intro-846844b5c9-cxqdg
6m3s        Normal    ScalingReplicaSet   deployment/web-intro              Scaled down replica set web-intro-846844b5c9 from 2 to 1
6m3s        Normal    Killing             pod/web-intro-846844b5c9-cxqdg    Stopping container web
6m3s        Normal    Created             pod/web-intro-54449bc466-vhrvv    Container created
6m3s        Normal    Pulled              pod/web-intro-54449bc466-vhrvv    Container image "nginx:1.29.0-alpine" already present on machine and can be accessed by the pod
6m2s        Normal    SuccessfulDelete    replicaset/web-intro-846844b5c9   Deleted pod: web-intro-846844b5c9-22cgf
6m2s        Normal    Killing             pod/web-intro-846844b5c9-22cgf    Stopping container web
6m2s        Normal    ScalingReplicaSet   deployment/web-intro              Scaled down replica set web-intro-846844b5c9 from 1 to 0
6m2s        Normal    Started             pod/web-intro-54449bc466-vhrvv    Container started
3m20s       Normal    Scheduled           pod/web-intro-846844b5c9-x6njk    Successfully assigned ft152-ud15/web-intro-846844b5c9-x6njk to minikube
77s         Normal    ScalingReplicaSet   deployment/web-intro              (combined from similar events): Scaled up replica set web-intro-6d4c975bcd from 0 to 1
3m20s       Normal    SuccessfulCreate    replicaset/web-intro-846844b5c9   Created pod: web-intro-846844b5c9-zskv9
3m20s       Normal    Killing             pod/web-intro-54449bc466-lbfqx    Stopping container web
3m20s       Normal    Pulled              pod/web-intro-846844b5c9-x6njk    Container image "nginx:1.28.0-alpine" already present on machine and can be accessed by the pod
3m20s       Normal    Created             pod/web-intro-846844b5c9-x6njk    Container created
3m20s       Normal    Started             pod/web-intro-846844b5c9-x6njk    Container started
3m20s       Normal    Scheduled           pod/web-intro-846844b5c9-zskv9    Successfully assigned ft152-ud15/web-intro-846844b5c9-zskv9 to minikube
3m20s       Normal    ScalingReplicaSet   deployment/web-intro              Scaled down replica set web-intro-54449bc466 from 3 to 2
3m20s       Normal    SuccessfulCreate    replicaset/web-intro-846844b5c9   Created pod: web-intro-846844b5c9-x6njk
3m20s       Normal    SuccessfulDelete    replicaset/web-intro-54449bc466   Deleted pod: web-intro-54449bc466-lbfqx
3m19s       Normal    Created             pod/web-intro-846844b5c9-zskv9    Container created
3m19s       Normal    SuccessfulCreate    replicaset/web-intro-846844b5c9   Created pod: web-intro-846844b5c9-4q8ks
3m19s       Normal    Pulled              pod/web-intro-846844b5c9-zskv9    Container image "nginx:1.28.0-alpine" already present on machine and can be accessed by the pod
3m19s       Normal    Started             pod/web-intro-846844b5c9-zskv9    Container started
3m19s       Normal    SuccessfulDelete    replicaset/web-intro-54449bc466   Deleted pod: web-intro-54449bc466-zmr2z
3m19s       Normal    Killing             pod/web-intro-54449bc466-zmr2z    Stopping container web
3m19s       Normal    Scheduled           pod/web-intro-846844b5c9-4q8ks    Successfully assigned ft152-ud15/web-intro-846844b5c9-4q8ks to minikube
3m18s       Normal    Created             pod/web-intro-846844b5c9-4q8ks    Container created
3m18s       Normal    Killing             pod/web-intro-54449bc466-vhrvv    Stopping container web
3m18s       Normal    Pulled              pod/web-intro-846844b5c9-4q8ks    Container image "nginx:1.28.0-alpine" already present on machine and can be accessed by the pod
3m18s       Normal    SuccessfulDelete    replicaset/web-intro-54449bc466   Deleted pod: web-intro-54449bc466-vhrvv
3m18s       Normal    Started             pod/web-intro-846844b5c9-4q8ks    Container started
77s         Normal    SuccessfulCreate    replicaset/web-intro-6d4c975bcd   Created pod: web-intro-6d4c975bcd-4929s
77s         Normal    Scheduled           pod/web-intro-6d4c975bcd-4929s    Successfully assigned ft152-ud15/web-intro-6d4c975bcd-4929s to minikube
37s         Normal    Pulling             pod/web-intro-6d4c975bcd-4929s    Pulling image "nginx:tag-ft152-che-non-esiste"
36s         Warning   Failed              pod/web-intro-6d4c975bcd-4929s    Failed to pull image "nginx:tag-ft152-che-non-esiste": rpc error: code = NotFound desc = failed to pull and unpack image "docker.io/library/nginx:tag-ft152-che-non-esiste": failed to resolve reference "docker.io/library/nginx:tag-ft152-che-non-esiste": docker.io/library/nginx:tag-ft152-che-non-esiste: not found
36s         Warning   Failed              pod/web-intro-6d4c975bcd-4929s    Error: ErrImagePull
10s         Normal    BackOff             pod/web-intro-6d4c975bcd-4929s    Back-off pulling image "nginx:tag-ft152-che-non-esiste"
10s         Warning   Failed              pod/web-intro-6d4c975bcd-4929s    Error: ImagePullBackOff
```

### Recupero del guasto: immagine iniziale e tre repliche

```text
2026-11-04T10:26:52+01:00
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                SELECTOR
deployment.apps/web-intro   3/3     3            3           24m   web          nginx:1.28.0-alpine   app=web-intro

NAME                                   DESIRED   CURRENT   READY   AGE     CONTAINERS   IMAGES                           SELECTOR
replicaset.apps/web-intro-54449bc466   0         0         0       6m44s   web          nginx:1.29.0-alpine              app=web-intro,pod-template-hash=54449bc466
replicaset.apps/web-intro-6d4c975bcd   0         0         0       109s    web          nginx:tag-ft152-che-non-esiste   app=web-intro,pod-template-hash=6d4c975bcd
replicaset.apps/web-intro-846844b5c9   3         3         3       24m     web          nginx:1.28.0-alpine              app=web-intro,pod-template-hash=846844b5c9

NAME                             READY   STATUS    RESTARTS   AGE     IP            NODE       NOMINATED NODE   READINESS GATES
pod/web-intro-846844b5c9-4q8ks   1/1     Running   0          3m51s   10.244.0.11   minikube   <none>           <none>
pod/web-intro-846844b5c9-x6njk   1/1     Running   0          3m53s   10.244.0.9    minikube   <none>           <none>
pod/web-intro-846844b5c9-zskv9   1/1     Running   0          3m52s   10.244.0.10   minikube   <none>           <none>
```

### Fine guidato: file e cluster a una replica

```text
2026-11-04T10:27:32+01:00
# Micro-demo: Nginx standard, non il frontend completo del Catalogo.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-intro
  namespace: ft152-ud15
spec:
  replicas: 1
  # Conserviamo i template precedenti per l'esercizio di rollback.
  revisionHistoryLimit: 5
  selector:
    matchLabels:
      app: web-intro
  template:
    metadata:
      labels:
        app: web-intro
    spec:
      containers:
        - name: web
          image: nginx:1.28.0-alpine
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 80
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                SELECTOR
deployment.apps/web-intro   1/1     1            1           25m   web          nginx:1.28.0-alpine   app=web-intro

NAME                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/web-intro   ClusterIP   10.98.208.71   <none>        80/TCP    12m   app=web-intro

NAME                             READY   STATUS    RESTARTS   AGE     IP           NODE       NOMINATED NODE   READINESS GATES
pod/web-intro-846844b5c9-x6njk   1/1     Running   0          4m33s   10.244.0.9   minikube   <none>           <none>
```

### Conclusione del guidato: riferimento conservato

```text
2026-11-04T10:28:01+01:00
# Micro-demo: Nginx standard, non il frontend completo del Catalogo.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-intro
  namespace: ft152-ud15
spec:
  replicas: 1
  # Conserviamo i template precedenti per l'esercizio di rollback.
  revisionHistoryLimit: 5
  selector:
    matchLabels:
      app: web-intro
  template:
    metadata:
      labels:
        app: web-intro
    spec:
      containers:
        - name: web
          image: nginx:1.28.0-alpine
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 80
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                SELECTOR
deployment.apps/web-intro   1/1     1            1           25m   web          nginx:1.28.0-alpine   app=web-intro

NAME                                   DESIRED   CURRENT   READY   AGE     CONTAINERS   IMAGES                           SELECTOR
replicaset.apps/web-intro-54449bc466   0         0         0       7m53s   web          nginx:1.29.0-alpine              app=web-intro,pod-template-hash=54449bc466
replicaset.apps/web-intro-6d4c975bcd   0         0         0       2m58s   web          nginx:tag-ft152-che-non-esiste   app=web-intro,pod-template-hash=6d4c975bcd
replicaset.apps/web-intro-846844b5c9   1         1         1       25m     web          nginx:1.28.0-alpine              app=web-intro,pod-template-hash=846844b5c9

NAME                             READY   STATUS    RESTARTS   AGE    IP           NODE       NOMINATED NODE   READINESS GATES
pod/web-intro-846844b5c9-x6njk   1/1     Running   0          5m2s   10.244.0.9   minikube   <none>           <none>
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "5"
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"name":"web-intro","namespace":"ft152-ud15"},"spec":{"replicas":1,"revisionHistoryLimit":5,"selector":{"matchLabels":{"app":"web-intro"}},"template":{"metadata":{"labels":{"app":"web-intro"}},"spec":{"containers":[{"image":"nginx:1.28.0-alpine","imagePullPolicy":"IfNotPresent","name":"web","ports":[{"containerPort":80,"name":"http"}]}]}}}}
  creationTimestamp: "2026-11-04T09:02:28Z"
  generation: 8
  name: web-intro
  namespace: ft152-ud15
  resourceVersion: "2466"
  uid: 2f1431ab-3a7f-4cc2-87ca-4f4b6164cfcf
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  revisionHistoryLimit: 5
  selector:
    matchLabels:
      app: web-intro
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: web-intro
    spec:
      containers:
      - image: nginx:1.28.0-alpine
        imagePullPolicy: IfNotPresent
        name: web
        ports:
        - containerPort: 80
          name: http
          protocol: TCP
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
  availableReplicas: 1
  conditions:
  - lastTransitionTime: "2026-11-04T09:19:02Z"
    lastUpdateTime: "2026-11-04T09:19:02Z"
    message: Deployment has minimum availability.
    reason: MinimumReplicasAvailable
    status: "True"
    type: Available
  - lastTransitionTime: "2026-11-04T09:02:28Z"
    lastUpdateTime: "2026-11-04T09:26:35Z"
    message: ReplicaSet "web-intro-846844b5c9" has successfully progressed.
    reason: NewReplicaSetAvailable
    status: "True"
    type: Progressing
  observedGeneration: 8
  readyReplicas: 1
  replicas: 1
  terminatingReplicas: 0
  updatedReplicas: 1
Name:                     web-intro
Namespace:                ft152-ud15
Labels:                   <none>
Annotations:              <none>
Selector:                 app=web-intro
Type:                     ClusterIP
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.98.208.71
IPs:                      10.98.208.71
Port:                     http  80/TCP
TargetPort:               http/TCP
Endpoints:                10.244.0.9:80
Session Affinity:         None
Internal Traffic Policy:  Cluster
Events:                   <none>
apiVersion: v1
items:
- addressType: IPv4
  apiVersion: discovery.k8s.io/v1
  endpoints:
  - addresses:
    - 10.244.0.9
    conditions:
      ready: true
      serving: true
      terminating: false
    nodeName: minikube
    targetRef:
      kind: Pod
      name: web-intro-846844b5c9-x6njk
      namespace: ft152-ud15
      uid: d6ffbb07-ed6f-4d02-b069-4c7bcb8329dd
  kind: EndpointSlice
  metadata:
    annotations:
      endpoints.kubernetes.io/last-change-trigger-time: "2026-11-04T09:27:15Z"
    creationTimestamp: "2026-11-04T09:15:05Z"
    generateName: web-intro-
    generation: 27
    labels:
      endpointslice.kubernetes.io/managed-by: endpointslice-controller.k8s.io
      kubernetes.io/service-name: web-intro
    name: web-intro-zxhbp
    namespace: ft152-ud15
    ownerReferences:
    - apiVersion: v1
      blockOwnerDeletion: true
      controller: true
      kind: Service
      name: web-intro
      uid: e2b59c3c-6fdf-488e-8c85-9def21deb4b7
    resourceVersion: "2465"
    uid: 3d7572ea-2acc-4dad-8464-065c21ebfc16
  ports:
  - name: http
    port: 80
    protocol: TCP
kind: List
metadata:
  resourceVersion: ""
State Recv-Q Send-Q Local Address:Port Peer Address:Port
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

```
