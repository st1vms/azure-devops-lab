# UD10 — Risposte alle domande sui concetti

## 1. Qual è la differenza fra codice sorgente, image e container?

**Risposta:** Il codice sorgente è l'insieme dei file di progetto scritti dal programmatore, come il file Python. L'image è un artefatto immutabile e pronto all'uso che include il codice, il runtime e le configurazioni. Il container è l'istanza in esecuzione creata a partire da un'image.

## 2. Che cosa fa `docker build` e che cosa non fa?

**Risposta:** Il comando `docker build` legge un Dockerfile e un contesto di build per creare un'image Docker. Non avvia e non esegue l'applicazione.

## 3. Che ruolo hanno Dockerfile, build context e `.dockerignore` nella creazione di un'image?

**Risposta:** Il Dockerfile è la ricetta con le istruzioni per costruire l'image. Il build context è l'insieme dei file della directory che il builder può utilizzare durante la costruzione. Il file `.dockerignore` serve a escludere file e cartelle inutili o sensibili dal context.

## 4. Che cosa succede se l'image indicata da `FROM` non è disponibile localmente?

**Risposta:** Se l'image indicata nell'istruzione `FROM` non è presente in locale, Docker prova a scaricarla automaticamente da un registry configurato, come Docker Hub.

## 5. Distingui `RUN` e `CMD`

**Risposta:** L'istruzione `RUN` esegue comandi e modifiche sul filesystem durante la fase di build dell'image. L'istruzione `CMD`, invece, definisce il comando predefinito che viene eseguito quando si avvia un container da quell'image.

## 6. Perché una modifica a `server.py` non modifica automaticamente un'image già costruita?

**Risposta:** Una modifica a `server.py` non altera l'image esistente perché il file viene copiato all'interno dell'image solo nel momento in cui viene eseguito il comando di build. Per aggiornare l'image occorre ricostruirla.

## 7. A che cosa serve il tag `catalog-backend:ud10`?

**Risposta:** Il tag `catalog-backend:ud10` serve a identificare l'image assegnandole un nome di repository (`catalog-backend`) e un'etichetta di versione o riferimento (`ud10`).

## 8. Che cosa succede, in ordine, quando eseguiamo `docker run catalog-backend:ud10`?

**Risposta:**  Quando si esegue `docker run catalog-backend:ud10`, Docker crea un nuovo container a partire dall'image specificata, applica le configurazioni di runtime ed esegue il comando predefinito associato (`CMD`).

## 9. Distingui `EXPOSE 8000` e `--publish 127.0.0.1:8000:8000`

**Risposta:** L'istruzione `EXPOSE 8000` inserita nel Dockerfile ha uno scopo puramente documentale per indicare la porta d'ascolto dell'applicazione. Il parametro `--publish 127.0.0.1:8000:8000` serve invece a pubblicare realmente la porta del container rendendola accessibile dall'host.

## 10. Che problema risolve Docker Compose rispetto a molti comandi `docker run` manuali?

**Risposta:** Docker Compose risolve la complessità e la ripetitività di dover digitare e gestire manualmente molti comandi separati di configurazione, reti, volumi e `docker run` per ogni singolo container.

## 11. Distingui il ruolo di un Dockerfile dal ruolo di `compose.yaml`

**Risposta:** Il Dockerfile descrive i passaggi necessari per costruire una singola image. Il file `compose.yaml` descrive invece in modo dichiarativo l'intero stack, coordinando più servizi, reti, volumi e dipendenze.

## 12. Che cosa crea/gestisce Compose nella nostra UD10?

**Risposta:** Nella UD10, Compose crea e gestisce una rete di bridge privata (`catalog-net`), un volume persistente (`catalog-runtime`) e i container per il backend e per il frontend.

## 13. Perché `docker compose up -d --build` può costruire sia backend sia frontend?

**Risposta:** Il comando `docker compose up -d --build` legge il file `compose.yaml`, individua i servizi che contengono le istruzioni di build e utilizza i rispettivi Dockerfile per costruire le relative image prima di avviare lo stack.

## 14. Perché il backend non viene pubblicato direttamente sull'host nello stack Compose?

**Risposta:** Il backend non viene esposto direttamente sull'host perché l'architettura prevede che il traffico passi attraverso il frontend Nginx, il quale fa da reverse proxy e inoltra le richieste alle API interne.

## 15. Perché Nginx usa `http://backend:8000` e non `http://localhost:8000`?

**Risposta:** Nginx usa `http://backend:8000` perché all'interno della rete Docker Compose i container si possono raggiungere tramite il nome del servizio grazie al DNS interno. Usare `localhost` farebbe riferimento al container frontend stesso.

## 16. Che funzione ha `catalog-net`?

**Risposta:** La rete `catalog-net` è una rete di tipo bridge che permette ai container del frontend e del backend di comunicare in modo isolato e sicuro tra loro utilizzando i nomi dei servizi.

## 17. Che funzione ha `catalog-runtime`?

**Risposta:** Il volume `catalog-runtime` permette di memorizzare i dati in una posizione indipendente dal ciclo di vita del container, garantendo la persistenza delle informazioni anche se il container viene rimosso o ricreato.

## 18. Perché `running` e `healthy` non significano la stessa cosa?

**Risposta:** Uno stato `running` indica semplicemente che il processo principale del container è attivo. Uno stato `healthy` indica invece che i controlli applicativi periodici definiti nell'healthcheck hanno dato esito positivo.

## 19. Che cosa fa `depends_on: condition: service_healthy` nel nostro stack?

**Risposta:** L'opzione `depends_on: condition: service_healthy` fa in modo che il frontend rimanga in attesa e si avvii soltanto dopo che il container del backend risulta non solo attivo, ma pienamente operativo e healthy.

## 20. Distingui rebuild e recreate

**Risposta:** Il rebuild prevede la ricostruzione dell'image a partire dal Dockerfile (necessario se cambia il codice o la configurazione di build). Il recreate prevede invece la distruzione e la creazione di un nuovo container riutilizzando la stessa image (utile se cambiano solo le variabili d'ambiente).

## 21. Quale ordine useresti per diagnosticare uno stack Compose che non risponde?

**Risposta:** Per diagnosticare uno stack che non risponde conviene procedere con ordine: controllare lo stato con `docker compose ps`, leggere i registri con `docker compose logs`, verificare la configurazione con `docker compose config` e controllare lo stato di salute, le reti e le porte.

## 22. In che modo ciò che facciamo manualmente in UD10 verrà riutilizzato nelle pipeline successive?

**Risposta:** Ciò che si fa manualmente in UD10 fornisce le basi e i concetti necessari che verranno poi automatizzati ed eseguiti all'interno delle pipeline di CI/CD tramite gli Agent per la build e il deployment.
