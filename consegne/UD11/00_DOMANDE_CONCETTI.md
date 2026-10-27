# UD11 — Risposte alle domande sui concetti

## 1. Distingui registry, repository, tag e digest

**Risposta:** Il registry è il servizio che ospita le immagini Docker. Il repository raggruppa le versioni della stessa applicazione. Il tag è un'etichetta leggibile (come `v1`), mentre il digest identifica univocamente e in modo immutabile il contenuto dell'immagine.

## 2. Perché non conviene basare una release solo sul tag `latest`?

**Risposta:** Perché `latest` è un'etichetta generica che può cambiare nel tempo e non garantisce la tracciabilità della versione esatta che si sta eseguendo.

## 3. Perché il login server ACR va letto dalla risorsa invece di costruirlo manualmente?

**Risposta:** Perché leggere il valore effettivo restituito da Azure evita errori umani e garantisce di utilizzare sempre l'indirizzo corretto del registry.

## 4. Qual è la differenza tra Container Apps Environment e Container App?

**Risposta:** L'Environment è il contesto infrastrutturale condiviso che ospita le applicazioni, mentre la Container App è la singola applicazione distribuita al suo interno con la sua configurazione.

## 5. Distingui revision e replica

**Risposta:** La revision rappresenta una versione immutabile della configurazione dell'applicazione. La replica è l'istanza concreta di quella revision in esecuzione sul sistema.

## 6. A che cosa serve ingress?

**Risposta:** Serve a esporre l'applicazione verso l'esterno, inoltrando il traffico HTTP in arrivo dal FQDN verso la porta interna del container.

## 7. Perché target port deve coincidere con la porta di ascolto dell'applicazione?

**Risposta:** Perché se non coincidono, il traffico dell'ingress viene inoltrato verso una porta sulla quale nessun processo applicativo è in ascolto, generando un errore.

## 8. Perché usare managed identity per il pull da ACR?

**Risposta:** Perché evita di inserire password o credenziali statiche nel codice, sfruttando la sicurezza nativa basata sulle identità gestite da Azure.

## 9. A che cosa serve `AcrPull`?

**Risposta:** Serve a concedere all'identità della Container App il permesso minimo necessario per leggere e scaricare l'immagine dal registry privato.

## 10. Che cosa succede tipicamente quando aggiorni l'image di una Container App?

**Risposta:** Viene creata automaticamente una nuova revision immutabile che riflette la modifica della configurazione o dell'immagine.

## 11. Perché in UD11 eseguiamo manualmente operazioni che verranno automatizzate in UD13–UD14?

**Risposta:** Per comprendere a fondo tutte le responsabilità e i passaggi operativi prima di codificarli all'interno delle pipeline.

## 12. Qual è la differenza fra RBAC Registry Permissions e RBAC+ABAC rispetto ai ruoli `AcrPull`/`AcrPush`?

**Risposta:** Nel modello con permessi RBAC classici si utilizzano ruoli come `AcrPull`, mentre nel modello RBAC+ABAC vengono impiegati ruoli specifici focalizzati sui singoli repository.

## 13. Perché il self-hosted Agent di UD09 non è necessario per svolgere UD11, pur essendo collegato alla progressione del corso?

**Risposta:** Perché in UD11 i comandi vengono eseguiti manualmente nel terminale locale, ma lo stesso ambiente WSL2 e Docker saranno successivamente sfruttati dall'Agent.

## 14. Distingui system-assigned e user-assigned managed identity

**Risposta:** La system-assigned ha un ciclo di vita vincolato direttamente alla risorsa che la possiede. La user-assigned è una risorsa di identità autonoma che può essere creata e gestita separatamente.

## 15. Che cosa significa scale-to-zero?

**Risposta:** Significa che la Container App può azzerare completamente il numero delle repliche attive quando non riceve traffico, riducendo l'impiego delle risorse.

## 16. Quali controlli eseguiresti se il FQDN restituisce errore dopo una nuova revision?

**Risposta:** Verificherei lo stato dell'ingress, la correttezza della target port, la salute e lo stato della revision attiva, i log applicativi, la presenza del tag in ACR e i permessi della managed identity
