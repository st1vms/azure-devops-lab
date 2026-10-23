# UD10 — Verifica

## Parte A

1. B. un artefatto usato per creare container
2. B. il build context
3. B. documenta la porta prevista nell'immagine ma non sostituisce `-p`
4. B. host 127.0.0.1:8080 → container 80
5. B. nome del servizio
6. B. il container frontend stesso
7. B. rimuove anche i volumi del progetto
8. B. può essere running ma unhealthy

## Parte B

### 9. Distingui image, container e registry

Un'image è un artefatto immutabile che funge da progetto, il container è l'istanza in esecuzione creata a partire da quell'image, mentre il registry è il sistema di distribuzione da cui è possibile prelevare le image di base.

### 10. Spiega perché il build context dovrebbe essere limitato

Il build context dovrebbe essere limitato per evitare di inviare al builder file inutili o sensibili presenti nel progetto, migliorando l'efficienza e la pulizia della costruzione tramite l'uso di un file

### 11. Distingui named volume e bind mount

Il named volume è uno spazio gestito da Docker che permette ai dati di persistere in modo indipendente dal ciclo di vita del singolo container, consentendo di mantenere le informazioni anche se il container viene rimosso.

### 12. Perché le variabili d'ambiente permettono di riusare la stessa immagine?

Le variabili d'ambiente permettono di riusare la stessa image perché definiscono i parametri di configurazione al momento del runtime (quando il container parte) e non durante la build, evitando di dover ricostruire l'artefatto per ogni modifica di configurazione.

### 13. Perché il backend Compose non deve necessariamente pubblicare una porta sull'host?

Il backend non deve necessariamente pubblicare una porta sull'host perché comunica all'interno di una rete privata Docker con il frontend, il quale riceve le richieste dall'esterno e le inoltra internamente al servizio backend.

### 14. Quali comandi useresti per iniziare il troubleshooting di uno stack Compose che non risponde?

Per iniziare il troubleshooting di uno stack Compose che non risponde si usano comandi di osservazione come `docker compose ps` per verificare lo stato e i container attivi, e `docker compose logs` per esaminare i messaggi scritti dai processi.

## Parte C

> docker compose ps mostra frontend Running e backend Restarting. Il browser restituisce 502. Nei log backend compare LOW_STOCK_THRESHOLD deve essere un intero, ricevuto: 'abc'.

### 15. Qual è la causa più probabile e qual è la modifica minima?

La causa più probabile è un errore di configurazione a runtime, in cui la variabile d'ambiente `LOW_STOCK_THRESHOLD` è stata impostata con una stringa non valida anziché con un numero intero. La modifica minima consiste nel correggere direttamente il valore all'interno del file `compose.yaml`, senza dover modificare il codice sorgente.

### 16. È necessario ricostruire l'immagine? Quali verifiche eseguiresti dopo la correzione?

Non è necessario ricostruire l'immagine, poiché il problema riguarda la configurazione runtime e non la struttura dell'artefatto. Dopo la modifica, le verifiche da eseguire comprendono l'uso di `docker compose up -d` per ricreare il container, seguito da `docker compose ps` e `docker compose logs` per confermare che il backend sia tornato nello stato healthy.

## 17. Una futura pipeline gira su `pool-ud09-wsl` e lo step `docker build` fallisce con errore di connessione al Docker daemon. Quale componente dell'ambiente controlleresti per primo e perché?

Il primo componente da controllare è l'integrazione di Docker Desktop con la distribuzione WSL2. Un errore di connessione al Docker daemon significa che la CLI all'interno dell'Agent self-hosted non riesce a comunicare con il motore Docker locale.

## 18. Distingui, rispetto alla disponibilità dei tool, un self-hosted Agent da un Microsoft-hosted Agent

Un self-hosted Agent si basa su un ambiente persistente e gestito internamente dove i tool sono installati stabilmente sotto il nostro controllo, mentre un Microsoft-hosted Agent fornisce un ambiente pulito e preconfigurato da Microsoft per ogni singolo Job, i cui strumenti dipendono esclusivamente dall'immagine di base utilizzata.

## Cleanup finale

- `docker compose down`:

```bash
✔ Container catalogo-prodotti-frontend-1 Removed                                                                                                                       0.3s
✔ Container catalogo-prodotti-backend-1  Removed                                                                                                                      10.3s
✔ Network catalogo-prodotti_catalog-net  Removed
```

- volume presente dopo `down`: Si
- `docker compose down -v`:

```bash
✔ Volume catalogo-prodotti_catalog-runtime Removed
```

- volume rimosso: Si
- immagini UD10 rimosse: Si
- prune globale usato: NO
