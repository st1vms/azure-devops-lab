# UD11 — Verifica

## Parte A

1. B. repository
2. B. leggerlo con `az acr show --query loginServer`
3. A. il nome della risorsa ACR
4. B. uno snapshot immutabile di una versione/configurazione della app
5. A. una istanza in esecuzione di una revision
6. A. managed identity
7. B. pull delle immagini dal registry nel modello RBAC appropriato
8. B. la app può scalare a zero repliche quando non necessarie

## Parte B

### 9. Distingui tag e digest

**Risposta:** Un tag è un'etichetta leggibile collegata a un'immagine, mentre il digest è un codice unico che identifica esattamente il suo contenuto.

### 10. Distingui Container Apps Environment, Container App, revision e replica

**Risposta:** L'Environment è lo spazio condiviso, la Container App è il servizio configurato, la revision è una versione bloccata e la replica è l'istanza che gira davvero.

### 11. Perché il corso usa managed identity invece di ACR admin credentials?

**Risposta:** Il corso sceglie le managed identity per evitare di usare credenziali fisse e sfruttare i ruoli di Azure in modo più sicuro.

### 12. Perché una nuova image normalmente produce una nuova revision?

**Risposta:** Perché ogni modifica all'immagine cambia la configurazione dell'applicazione, spingendo la piattaforma a creare una nuova versione.

### 13. Che cosa deve coincidere tra backend e ingress target port?

**Risposta:** Devono corrispondere la porta interna usata dall'applicazione e la porta d'ingresso configurata nella piattaforma.

### 14. Elenca almeno cinque controlli per una Container App non raggiungibile

**Risposta:** Controllare se l'ingresso esterno è attivo, se la porta corrisponde, se la revisione è attiva, se ci sono repliche e cosa dicono i log.

### 15. Perché il laboratorio UD11 esegue manualmente build, push e deployment invece di partire subito da una pipeline?

**Risposta:** Per capire bene ogni singolo passaggio manuale prima di affidarlo alle pipeline automatiche.

### 16. Se un registry è configurato in modalità RBAC+ABAC, perché non puoi dare per scontato che `AcrPull` sia il ruolo corretto?

**Risposta:** Perché con quel sistema i ruoli standard come AcrPull potrebbero non bastare o funzionare diversamente sui repository.

### 17. In che modo il lavoro manuale di UD11 prepara UD13 e UD14?

**Risposta:** Perché ci fa capire i comandi e la logica che poi gli script e gli agenti ripeteranno in automatico.

### 18. Distingui system-assigned e user-assigned managed identity

**Risposta:** Quella di sistema ha la vita legata alla risorsa che la possiede, mentre quella creata dall'utente è indipendente e riutilizzabile.

## Parte C

> ACR contiene `catalog-backend:v2`. La revision corrente è Healthy. I log mostrano `listening` on `0.0.0.0:8000`. L'ingress è external ma `targetPort=9000`. Il FQDN restituisce errore.

### 19. Qual è la causa più probabile e qual è la correzione minima?

**Risposta:** La causa più probabile è che l'ingress inoltra il traffico sulla porta 9000, mentre l'applicazione è in ascolto sulla porta 8000. La correzione minima consiste nell'aggiornare la configurazione dell'ingress impostando la porta di destinazione su 8000.

### 20. Quali verifiche eseguiresti dopo la correzione prima di dichiarare risolto il problema?

**Risposta:** Dopo la correzione verificherei che l'ingress usi la porta corretta, controllerei che la revisione sia attiva e in stato sano, e proverei a interrogare l'endpoint FQDN per ricevere una risposta corretta dall'applicazione.

## Cleanup finale

- resource list verificata: Si
- Resource Group eliminato: Si
- `az group exists` = false: Si
- immagini Docker locali UD11 rimosse: Si
- prune globale usato: NO
