# UD15 — Risposte e prova individuale

Partecipante, data/ora/fuso: Stefano Raneri, 2026-11-04 10:55 CET

## Domande di raccordo architetturale

- **Chi avvia il container dopo apply e chi decide il nodo?**
Dopo `kubectl apply`, lo Scheduler decide su quale nodo assegnare il Pod (nel nostro caso `minikube`). Sul nodo scelto, il kubelet legge l'assegnazione e chiede al runtime dei container (`containerd`) di scaricare l'immagine e avviare il container.

- **Perché tre Pod sul Minikube non dimostrano alta disponibilità?**
I tre Pod girano tutti dentro lo stesso unico nodo locale `minikube`. Se questo nodo o Docker sul computer si bloccano, tutti e tre i Pod smettono di funzionare contemporaneamente.

## 1. Domande

1. Il controller del ReplicaSet nota che c'è un solo Pod invece di tre e crea i due oggetti Pod mancanti. Lo Scheduler interviene subito dopo per assegnare questi nuovi Pod a un nodo libero e idoneo del cluster.

2. L'API Server riceve il file YAML da `kubectl` e salva la configurazione in `etcd`. Il kubelet gira sul nodo, vede che gli è stato assegnato un Pod e ordina al runtime (`containerd`) di scaricare l'immagine e far partire il processo Nginx.

3. Il Pod esegue il container, il ReplicaSet mantiene il numero giusto di copie del Pod e il Deployment gestisce gli aggiornamenti e la cronologia dei ReplicaSet. Nel laboratorio modifichiamo sempre il Deployment.

4. Il nome non collega gli oggetti tra loro. Devo confrontare il campo `selector` del Service con le `labels` assegnate ai Pod (ad esempio `app=web-intro`) e verificare che siano nello stesso namespace e che i Pod siano `Ready`.

5. Il `kube-context` dice a `kubectl` quale cluster e quale utente usare, mentre il `namespace` è la cartella virtuale dentro quel cluster dove si trovano gli oggetti. Li scriviamo sempre nei comandi per non sbagliare ambiente o modificare risorse nel posto sbagliato.

6. No, `containerPort: 80` è solo una porta interna al Pod e informativa. Per vedere la pagina da Windows abbiamo usato `kubectl port-forward`, che crea un tunnel temporaneo tra una porta locale del PC (come 8081 o 8082) e la porta del Pod.

7. Con lo scaling cambia solo il numero di Pod dentro lo stesso ReplicaSet e il numero di revisione non cambia. Con l'aggiornamento dell'immagine, invece, il Deployment crea un ReplicaSet nuovo, avvia una nuova revisione e spegne i Pod del vecchio ReplicaSet.

8. Sì, è possibile grazie al RollingUpdate. Quando abbiamo messo il tag sbagliato `nginx:tag-ft152-che-non-esiste`, il nuovo Pod `web-intro-6d4c975bcd-4929s` si è bloccato in `ImagePullBackOff`, ma i tre Pod vecchi del ReplicaSet `web-intro-846844b5c9` sono rimasti `1/1 Running` a rispondere alle richieste.

9. Uso `logs --previous` quando un container è andato in crash e si è riavviato (`RESTARTS > 0`), per leggere cosa è successo prima dell'errore. Con `ImagePullBackOff` non serve a niente perché l'immagine non è stata scaricata e il container non è mai partito.

10. No, il rollback rimette solo il vecchio modello di Pod (come l'immagine precedente) dentro il cluster. Non tocca i file YAML salvati nella cartella di Git e non annulla le modifiche fatte ai dati dentro i volumi.

11. Non proteggono dalla perdita del nodo perché tutti e tre i Pod vivono sulla stessa macchina virtuale o container `minikube`. Rimane il rischio di un unico punto di rottura (Single Point of Failure): se cade il nodo, cade tutta l'applicazione.

12. No, oggi abbiamo avviato solo un server Nginx standard di prova. Per migrare il Catalogo completo mancano il collegamento di rete stabile verso il backend Python e un volume persistente per salvare i dati che il backend scrive in `/runtime`.

## 2. Lettura del cluster

Pod scelto, owner, immagine, nodo e condizione: Ho scelto il Pod `web-autonomo-85f6469d54-g5hwh` (IP `10.244.0.13`). Il suo owner è il ReplicaSet `web-autonomo-85f6469d54`, usa l'immagine `nginx:1.28.0-alpine`, gira sul nodo `minikube` ed è nello stato `Running` con condizione `Ready: True` (`1/1`).
Relazione con il Service ed EndpointSlice: Il Service `web-autonomo` ha il selector `app=web-autonomo` che trova i tre Pod della variante autonoma. L'EndpointSlice `web-autonomo-99rbp` registra infatti i loro tre indirizzi IP (`10.244.0.13`, `10.244.0.14`, `10.244.0.15`) sulla porta `80`, separandoli da quello di `web-intro` (`10.244.0.9`).
Cronologia letta e limite di ciò che prova: Il comando `rollout history` di `web-intro` mostra le revisioni `2`, `4` e `5`. Le revisioni `1` e `3` non ci sono più perché sono state sostituite quando siamo tornati a quei modelli. Questa lista mostra solo che il template è cambiato nel tempo, ma non ci dice quante repliche ci sono ora, se l'app funziona o cosa è scritto nel file YAML locale.

## 3. Consegne

File completi, percorsi manifest e commit: File di consegna compilati in `consegne/UD15/` (`00_INVENTARIO.md`, `01_GUIDATO.md`, `02_AUTONOMO.md`, `03_VERIFICA.md`) e manifest salvati in `k8s/ud15/`, pronti per il commit finale della UD15.
Prove operative mancanti da recuperare: Nessuna prova mancante; nell'ultimo output `web-autonomo` ha 3 repliche attive (`3/3`), quindi prima del commit finale va allineato a 2 repliche se richiesto dalla chiusura comune del §4.
Punteggio ricevuto e motivazione del recupero, se necessario: Autovalutazione 20/20; tutte le prove di scaling, cambio immagine, rollback e diagnosi dell'errore `ImagePullBackOff` sono state raccolte e verificate.
