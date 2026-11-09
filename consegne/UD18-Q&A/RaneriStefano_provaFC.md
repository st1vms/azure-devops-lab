# UD18 — Prova di consolidamento operativo · Piano B

## 90 minuti — 5 verifiche al terminale e 2 quesiti brevi

Obiettivo: ricostruire le fasi più significative del percorso attraverso il rintracciamento delle informazioni contenute nelle unità didattiche e nei laboratori svolti, verificando i risultati nell’ambiente disponibile.

Nome: Stefano Raneri  Data: 09/11/2026

Puoi consultare materiali e attività già svolte: individua tu dove cercare. Rispondi in 2–3 righe per quesito, tenendo comandi e output separati. Descrivi operazioni e risultati senza dover citare il percorso formativo. Usa il contesto minikube, namespace ft152-catalogo, con ambiente UD16/UD17 già avviato. Non eseguire deploy, cancellazioni o modifiche. Registra eventuali errori; se l’ambiente impedisce un’operazione, indica il comando che useresti e segnala che il risultato non è stato verificato. Non consegnare credenziali o token.

*(\*) Errori relativi a distribuzione Linux incompatibile con docker*

## Blocco 1 — Stato, configurazione e dati

Tempo indicativo per completare il blocco: **40 minuti**.

### P01 — Immagine e stato

Nel namespace ft152-catalogo individua l’immagine configurata per il backend e controlla lo stato dei suoi Pod. Riporta nome e tag dell’immagine, repliche pronte e un risultato che giustifichi la tua conclusione. Spiega perché la sola immagine configurata nel Deployment non dimostra che il servizio funzioni.

**Risposta:** La sola presenza di un'immagine configurata nel Deployment attesta soltanto il software dichiarato ma non garantisce che il container sia avviato, superi le probe e risulti pronto a ricevere traffico dal Service. Per confermare il funzionamento occorre verificare che le repliche siano effettivamente pronte (Ready) e che l'applicazione risponda.

**Comando o configurazione richiesta:**

```bash
kubectl --context=minikube -n ft152-catalogo get deployment backend -o jsonpath='{.spec.template.spec.containers[0].image}'
```

```bash
kubectl --context=minikube -n ft152-catalogo get pods -l app=backend -o wide
```

**Risultato osservato (estratto utile):**

Comando 1:

```bash
catalog-backend:ud16
```

Comando 2:

```bash
NAME                     READY   STATUS    RESTARTS       AGE     IP           NODE       NOMINATED NODE   READINESS GATES
backend-5cfd7c8c-qmzs4   1/1     Running   1 (5m4s ago)   3d23h   10.244.0.3   minikube   <none>           <none>
```

**Materiale consultato (file e paragrafo):**

`UD17/partecipanti/k8s/ud17/backend.yaml` e `UD17/partecipanti/02_LAB_GUIDATO.md` (paragrafo sullo stato di partenza).

### P02 — Configurazione

Recupera LOW_STOCK_THRESHOLD dal ConfigMap catalog-config e verifica il valore presente nell’ambiente del container backend. Confronta i due risultati e spiega se modificare il ConfigMap aggiornerebbe automaticamente la variabile nel processo già avviato. Non modificare la configurazione.

**Risposta:** Il ConfigMap definisce il valore della soglia, che viene iniettato come variabile d'ambiente all'avvio del container. Modificare il ConfigMap non aggiorna automaticamente la variabile nel processo Python già in esecuzione, poiché le variabili d'ambiente vengono lette una sola volta al bootstrap.

**Comando o configurazione richiesta:**

```bash
kubectl --context=minikube -n ft152-catalogo get configmap catalog-config -o yaml
```

```bash
kubectl --context=minikube -n ft152-catalogo exec deployment/backend -- printenv LOW_STOCK_THRESHOLD
```

**Risultato osservato (estratto utile):**

Comando 1:

```bash
apiVersion: v1
data:
  APP_HOST: 0.0.0.0
  APP_PORT: "8000"
  LOW_STOCK_THRESHOLD: "5"
  RUNTIME_DIR: /runtime
kind: ConfigMap
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","data":{"APP_HOST":"0.0.0.0","APP_PORT":"8000","LOW_STOCK_THRESHOLD":"5","RUNTIME_DIR":"/runtime"},"kind":"ConfigMap","metadata":{"annotations":{},"name":"catalog-config","namespace":"ft152-catalogo"}}
  creationTimestamp: "2026-11-04T16:06:26Z"
  name: catalog-config
  namespace: ft152-catalogo
  resourceVersion: "4680"
  uid: 7d9335a1-ea02-4989-bf95-1e2190856dc6
```

Comando 2:

```bash
5
```

**Materiale consultato (file e paragrafo):**

`UD16/partecipanti/00_CONCETTI.md` (paragrafo "Immagine e configurazione: due responsabilità diverse").

### P03 — Dato persistente

Individua il PVC usato dal backend, verifica dove viene montato e leggi il file del contatore in /runtime. Spiega che cosa dimostrano questi controlli sulla persistenza e quale prova ulteriore servirebbe per verificarla dopo una ricreazione. Non eliminare Pod o volumi e non chiamare l’endpoint del contatore.

**Risposta:** Il backend utilizza un PVC montato in `/runtime`, dove viene salvato il file del contatore. Questo dimostra che il dato è associato a uno storage persistente esterno al container, ma per verificarne la sopravvivenza occorre eliminare il Pod e verificare che il nuovo Pod legga lo stesso valore dal file.

**Comando o configurazione richiesta:**

```bash
kubectl --context=minikube -n ft152-catalogo get deployment backend -o yaml | grep -A 10 volumeMounts
```

```bash
kubectl --context=minikube -n ft152-catalogo exec deployment/backend -- cat /runtime/counter.txt
```

**Risultato osservato (estratto utile):**

Comando 1:

```bash
{"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"name":"backend","namespace":"ft152-catalogo"},"spec":{"replicas":1,"selector":{"matchLabels":{"app":"backend"}},"strategy":{"type":"Recreate"},"template":{"metadata":{"labels":{"app":"backend"}},"spec":{"containers":[{"env":[{"name":"DEMO_SECRET","valueFrom":{"secretKeyRef":{"key":"demo","name":"catalog-demo"}}}],"envFrom":[{"configMapRef":{"name":"catalog-config"}}],"image":"catalog-backend:ud16","imagePullPolicy":"IfNotPresent","name":"backend","ports":[{"containerPort":8000,"name":"http"}],"resources":{"limits":{"cpu":"200m","memory":"128Mi"},"requests":{"cpu":"20m","memory":"64Mi"}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]}},"volumeMounts":[{"mountPath":"/runtime","name":"runtime"},{"mountPath":"/etc/catalog-config","name":"config-file","readOnly":true}]}],"securityContext":{"fsGroup":10001,"runAsGroup":10001,"runAsNonRoot":true,"runAsUser":10001,"seccompProfile":{"type":"RuntimeDefault"}},"volumes":[{"configMap":{"name":"catalog-config"},"name":"config-file"},{"name":"runtime","persistentVolumeClaim":{"claimName":"catalog-runtime"}}]}}}}
  creationTimestamp: "2026-11-05T10:56:11Z"
  generation: 1
  name: backend
  namespace: ft152-catalogo
  resourceVersion: "24624"
  uid: e11cb844-1ba1-44f2-a50d-32e6bc906965
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  revisionHistoryLimit: 10
--
        volumeMounts:
        - mountPath: /runtime
          name: runtime
        - mountPath: /etc/catalog-config
          name: config-file
          readOnly: true
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext:
        fsGroup: 10001
```

Comando 2:

```bash
3
```

**Materiale consultato (file e paragrafo):**

`UD16/partecipanti/00_CONCETTI.md` (paragrafo "Perché un Pod nuovo non deve cancellare i dati").

## Blocco 2 — Rete e risposta applicativa

Tempo indicativo per completare il blocco: **30 minuti**.

### P04 — Comunicazione interna

Dal Pod frontend verifica la risoluzione del nome backend. Controlla poi il Service backend e i relativi EndpointSlice: associa almeno un indirizzo a un Pod e alla sua condizione di disponibilità. Spiega perché risolvere il nome non basta a dimostrare che l’applicazione risponda.

**Risposta:** La risoluzione DNS verifica unicamente che il nome del Service venga tradotto in un indirizzo IP interno, ma non garantisce che il backend sia in ascolto sulla porta corretta o che l'applicazione risponda alle richieste HTTP. Per confermare la comunicazione occorre verificare il Service, i selettori e lo stato di prontezza (ready) degli EndpointSlice associati ai Pod.

**Comando o configurazione richiesta:**

```bash
kubectl --context=minikube -n ft152-catalogo exec deployment/frontend -- nslookup backend.ft152-catalogo.svc.cluster.local
```

```bash
kubectl --context=minikube -n ft152-catalogo get endpointslices -l kubernetes.io/service-name=backend
```

**Risultato osservato (estratto utile):**

Comando 1 (*):

```bash
error: unable to upgrade connection: container not found ("frontend")
```

Comando 2:

```bash
NAME            ADDRESSTYPE   PORTS   ENDPOINTS    AGE
backend-frplj   IPv4          8000    10.244.0.3   4d18h
```

**Materiale consultato (file e paragrafo):**

`UD16/partecipanti/00_CONCETTI.md` (paragrafo "DNS interno: un nome non è una risposta HTTP").

### P05 — Accesso HTTP e riscontri

Usa curl per interrogare /health e /api/products/P001 passando dall’accesso locale sulla porta 18016 con Host catalogo.lab. Riporta stato HTTP e un dato utile della risposta; consulta poi gli ultimi log del backend. Se un controllo fallisce, conserva l’errore e indica il controllo successivo pertinente, senza modificare l’ambiente.

**Risposta:** L'interrogazione tramite `curl` passando dall'accesso locale sulla porta `18016` con l'header `Host: catalogo.lab` verifica l'intero percorso di rete esterno (ingresso Docker, NodePort, proxy Gateway, frontend e backend).

**Comando o configurazione richiesta:**

```bash
curl -i -H "Host: catalogo.lab" http://127.0.0.1:18016/health
```

```bash
curl -i -H "Host: catalogo.lab" http://127.0.0.1:18016/api/products/P001
```

```bash
kubectl --context=minikube -n ft152-catalogo logs deployment/backend --tail=30
```

**Risultato osservato (estratto utile):**

Comando 1:

```bash
curl: (7) Failed to connect to 127.0.0.1 port 18016 after 0 ms: Could not connect to server
```

Comando 2:

```bash
curl: (7) Failed to connect to 127.0.0.1 port 18016 after 0 ms: Could not connect to server
```

Comando 3:

```bash
Catalog backend listening on http://0.0.0.0:8000 threshold=5 runtime=/runtime
```

**Materiale consultato (file e paragrafo):**

`UD16/partecipanti/02_LAB_GUIDATO.md` (paragrafo "La prova applicativa non dipende dal terminale").

## Blocco 3 — Raccontare e motivare le operazioni

Tempo indicativo per completare il blocco: **20 minuti**.

### S01 — Dalla pipeline alla versione in esecuzione

Devi spiegare a un referente tecnico come distribuisci una nuova versione del backend. Ricostruisci il passaggio dal commit alla build, alla pubblicazione in ACR e alla distribuzione; indica quale controllo usi per confermare la versione in esecuzione. Recupera dalla pipeline una configurazione che colleghi questi passaggi.

**Risposta:**

Per distribuire una nuova versione del backend, il codice sorgente viene sottoposto a commit e test nella pipeline CI, la quale compila l'immagine Docker e la pubblica nel registro ACR associandole un tag univoco basato sul Build ID. La fase di delivery aggiorna successivamente il Deployment nel cluster, e la versione effettivamente in esecuzione viene confermata verificando il tag dell'immagine associata al Pod o interrogando l'endpoint di salute.

**Comando o configurazione richiesta:**

```bash
kubectl --context=minikube -n ft152-catalogo get deployment backend -o jsonpath='{.spec.template.spec.containers[0].image}'
```

```bash
kubectl --context=minikube -n ft152-catalogo get pods -l app=backend -o jsonpath='{.items[0].spec.containers[0].image}'
```

**Risultato osservato (estratto utile):**

Immagine in esecuzione: `catalog-backend:ud16` (o il tag corrispondente alla build).

**Materiale consultato (file e paragrafo):**

`UD14/partecipanti/000A_RIPASSO_CI.md` (paragrafo "Dal sorgente all'immagine: che cosa produce la CI") e `UD14/partecipanti/00_CONCETTI.md`.

### S02 — Prima di modificare l’infrastruttura

Hai una configurazione Bicep e una Terraform già predisposte. Recupera per ciascuna il comando che permette di esaminare le modifiche previste prima di applicarle. Spiega quale risultato controlleresti dopo l’applicazione e a che cosa serve lo state di Terraform. Non eseguire le modifiche.

**Risposta:**

Prima di applicare modifiche, sia Terraform che Bicep mettono a disposizione comandi di pianificazione per esaminare in anteprima le variazioni pianificate rispetto allo stato attuale dell'infrastruttura. Terraform, in particolare, utilizza uno state remoto per memorizzare la mappatura tra le risorse reali e la configurazione dichiarata, garantendo la coerenza e il blocco concorrente (locking) nelle esecuzioni successive.

**Comando o configurazione richiesta:**

```bash
terraform plan
```

```bash
az deployment group what-if --resource-group <NOME_RG> --template-file <file.bicep>
```

**Risultato osservato (estratto utile):**

Output del comando di piano ( `terraform plan` o `what-if`) che elenca in modo analitico le risorse da aggiungere, modificare o rimuovere.

**Materiale consultato (file e paragrafo):**

`UD14/partecipanti/00_CONCETTI.md` (paragrafo "Terraform plan prima della build").
