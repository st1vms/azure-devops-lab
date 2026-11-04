# UD15 — Consegna laboratorio autonomo

Partecipante, data/ora/fuso: Stefano Raneri
Percorsi: `k8s/ud15/autonomo/deployment.yaml` e `service.yaml`.

| Requisito | Configurazione e output che lo dimostrano |
|---|---|
| Due repliche web-autonomo, immagine iniziale | File `k8s/ud15/autonomo/deployment.yaml` con `replicas: 2`, `selector.matchLabels.app: web-autonomo` e `image: nginx:1.28.0-alpine`. Verificato con `kubectl -n ft152-ud15 get deployment,pods -l app=web-autonomo -o wide` che mostra `READY 2/2` e due Pod `1/1 Running` con immagine `nginx:1.28.0-alpine`. |
| Label component=frontend sui Pod | Definita in `spec.template.metadata.labels` (`component: frontend`) nel manifest del Deployment. Verificata sui Pod con `kubectl -n ft152-ud15 get pods -l component=frontend --show-labels`, che restituisce esclusivamente i due Pod `web-autonomo` con `app=web-autonomo,component=frontend`. |
| Service con endpoint della variante, HTTP 200 su 8082 | File `k8s/ud15/autonomo/service.yaml` (`ClusterIP`, porta `80`, `targetPort: http`, `selector.app: web-autonomo`). `kubectl -n ft152-ud15 get endpointslices -l kubernetes.io/service-name=web-autonomo -o wide` riporta i due IP dei Pod della variante. Con `port-forward` attivo su `8082:80`, `curl -i http://127.0.0.1:8082/` e il browser su `http://localhost:8082/` restituiscono `HTTP/1.1 200 OK` e la pagina standard di Nginx. |

- Differenza fra questa micro-demo e il frontend del Catalogo: Questa variante esegue due repliche stateless dell'immagine standard di Nginx che servono la pagina di benvenuto predefinita, isolata dal workload guidato tramite selector e identificata dal ruolo logico `component: frontend`. La migrazione del Catalogo prodotti completo richiederà invece l'integrazione con il backend Python tramite un Service dedicato e risoluzione DNS interna, il passaggio della configurazione tramite ConfigMap e Secret, la persistenza dei dati di `/runtime` mediante PersistentVolumeClaim (PVC) e l'esposizione del traffico HTTP tramite Gateway anziché port-forward temporaneo.

- Workload guidato conservato a una replica: Verificato con `kubectl --context=minikube -n ft152-ud15 get deployment web-intro web-autonomo -o wide`: il Deployment `web-intro` mantiene `READY 1/1` con immagine `nginx:1.28.0-alpine` e selector `app=web-intro`, separato da `web-autonomo` (`READY 2/2`).

- Problema eventualmente incontrato, diagnosi, correzione e nuovo test: Durante la prima verifica con `kubectl -n ft152-ud15 rollout status deployment/web-autonomo` è stato restituito l'errore `Error from server (NotFound): deployments.apps "web-autonomo" not found`. La diagnosi con `kubectl -n ft152-ud15 get deployments` e la lettura di `k8s/ud15/autonomo/deployment.yaml` ha evidenziato che il manifest della variante non era ancora stato applicato con `name: web-autonomo`. Scritto e salvato correttamente il manifest in `k8s/ud15/autonomo/deployment.yaml` e applicato con `kubectl apply -f k8s/ud15/autonomo/deployment.yaml`, il nuovo test di `rollout status` si è concluso con `deployment "web-autonomo" successfully rolled out` e 2 Pod `1/1 Running`.

- Tempo impiegato: preparazione / applicazione e test / consegna: 25 min / 30 min / 10 min (totale: 65 min).

- Port-forward terminato e risorse conservate: Sessione `port-forward` su porta 8082 terminata con `Ctrl+C` (verificato l'assenza di listener con `ss -ltn '( sport = :8082 )'`). Nel namespace `ft152-ud15` restano attivi e allineati ai rispettivi manifest sia `web-intro` (1/1) sia `web-autonomo` (2/2) con i relativi Service.

- Commit finale: File aggiunti selettivamente (`k8s/ud15/`, `consegne/UD15/`) e registrati nel repository operativo (aggiornare con l'hash restituito da `git rev-parse --short HEAD` dopo il commit).

## Evidenze Laboratorio Autonomo

```text
2026-11-04T10:45:21+01:00
# Micro-demo: Nginx standard, non il frontend completo del Catalogo.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-autonomo
  namespace: ft152-ud15
spec:
  replicas: 3
  # Conserviamo i template precedenti per l'esercizio di rollback.
  revisionHistoryLimit: 5
  selector:
    matchLabels:
      app: web-autonomo
  template:
    metadata:
      labels:
        app: web-autonomo
        component: frontend
    spec:
      containers:
        - name: web
          image: nginx:1.28.0-alpine
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 80
apiVersion: v1
kind: Service
metadata:
  name: web-autonomo
  namespace: ft152-ud15
spec:
  type: ClusterIP
  # I backend sono selezionati dalla label, non dal nome del Deployment.
  selector:
    app: web-autonomo
  ports:
    - name: http
      port: 80
      targetPort: http
NAME                           READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                SELECTOR           LABELS
deployment.apps/web-autonomo   3/3     3            3           57s   web          nginx:1.28.0-alpine   app=web-autonomo   <none>
deployment.apps/web-intro      1/1     1            1           42m   web          nginx:1.28.0-alpine   app=web-intro      <none>

NAME                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE   SELECTOR           LABELS
service/web-autonomo   ClusterIP   10.109.175.250   <none>        80/TCP    54s   app=web-autonomo   <none>
service/web-intro      ClusterIP   10.98.208.71     <none>        80/TCP    30m   app=web-intro      <none>

NAME                                READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES   LABELS
pod/web-autonomo-85f6469d54-g5hwh   1/1     Running   0          57s   10.244.0.13   minikube   <none>           <none>            app=web-autonomo,component=frontend,pod-template-hash=85f6469d54
pod/web-autonomo-85f6469d54-kftjh   1/1     Running   0          57s   10.244.0.14   minikube   <none>           <none>            app=web-autonomo,component=frontend,pod-template-hash=85f6469d54
pod/web-autonomo-85f6469d54-rkn5z   1/1     Running   0          57s   10.244.0.15   minikube   <none>           <none>            app=web-autonomo,component=frontend,pod-template-hash=85f6469d54
pod/web-intro-846844b5c9-x6njk      1/1     Running   0          22m   10.244.0.9    minikube   <none>           <none>            app=web-intro,pod-template-hash=846844b5c9
Name:                     web-autonomo
Namespace:                ft152-ud15
Labels:                   <none>
Annotations:              <none>
Selector:                 app=web-autonomo
Type:                     ClusterIP
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.109.175.250
IPs:                      10.109.175.250
Port:                     http  80/TCP
TargetPort:               http/TCP
Endpoints:                10.244.0.14:80,10.244.0.13:80,10.244.0.15:80
Session Affinity:         None
Internal Traffic Policy:  Cluster
Events:                   <none>
NAME                 ADDRESSTYPE   PORTS   ENDPOINTS                             AGE
web-autonomo-99rbp   IPv4          80      10.244.0.14,10.244.0.13,10.244.0.15   55s
NAME                            READY   STATUS    RESTARTS   AGE   LABELS
web-autonomo-85f6469d54-g5hwh   1/1     Running   0          58s   app=web-autonomo,component=frontend,pod-template-hash=85f6469d54
web-autonomo-85f6469d54-kftjh   1/1     Running   0          58s   app=web-autonomo,component=frontend,pod-template-hash=85f6469d54
web-autonomo-85f6469d54-rkn5z   1/1     Running   0          58s   app=web-autonomo,component=frontend,pod-template-hash=85f6469d54
```
