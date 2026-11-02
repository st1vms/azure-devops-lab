# UD14 — Domande concetti

## 1. Qual è la differenza tra CI e Continuous Delivery?

**Risposta:** La Continuous Integration (CI) si occupa di verificare il codice e costruire l'immagine del programma. La Continuous Delivery (CD) prende quell'immagine e la distribuisce automaticamente sull'infrastruttura in modo che sia pronta per l'uso.

## 2. Quale service connection utilizza la pipeline UD14?

**Risposta:** Usa una sola connessione di tipo Azure Resource Manager (`sc-azure-ud13-15`) basata su Workload Identity Federation, senza memorizzare password nel codice.

## 3. Perché la pipeline non utilizza `Docker@2`?

**Risposta:** Perché il task `Docker@2` richiede una connessione dedicata al registro dei container, mentre noi abbiamo scelto di usare un'unica service connection Azure e di autenticarci con i comandi della CLI.

## 4. Quale ruolo deve avere l'identità della pipeline sull'ACR?

**Risposta:** L'identità deve avere il ruolo `AcrPush` per poter caricare all'interno del registro le nuove immagini create dalla build.

## 5. Perché Terraform usa uno state remoto?

**Risposta:** Lo state remoto serve a memorizzare lo stato dell'infrastruttura fuori dalla macchina virtuale temporanea della pipeline, evitando che i dati vadano persi alla fine del lavoro.

## 6. Dove viene conservato lo state UD14?

**Risposta:** Viene conservato nel cloud all'interno di un Azure Storage Account, dentro a un container dedicato ai file di stato.

## 7. Quale ruolo permette alla pipeline di utilizzare lo state Blob?

**Risposta:** Il ruolo `Storage Blob Data Contributor`, che dà i permessi necessari per leggere e scrivere il file di stato sullo storage.

## 8. Come si autentica Terraform durante la pipeline?

**Risposta:** Terraform viene eseguito all'interno di un blocco `AzureCLI@2` e sfrutta automaticamente la sessione già aperta e autenticata dalla service connection.

## 9. Quali risorse vengono lette come esistenti?

**Risposta:** Risorse come il Resource Group, il registro ACR e l'identità gestita vengono lette come risorse già pronte tramite i data source, senza ricrearle.

## 10. Quali risorse vengono gestite da Terraform?

**Risposta:** Terraform gestisce la creazione e la modifica dell'ambiente delle Container Apps e della Container App vera e propria.

## 11. Perché la Container App utilizza una managed identity?

**Risposta:** Usa un'identità gestita separata per poter accedere al registro in modo sicuro, applicando la regola di dare solo i permessi strettamente necessari.

## 12. Quale ruolo ha questa identità sull'ACR?

**Risposta:** Ha il ruolo `AcrPull`, che le permette soltanto di scaricare e leggere l'immagine del programma per poterla avviare.

## 13. Perché viene eseguito `terraform plan` nello stage iniziale?

**Risposta:** Per controllare che la configurazione sia corretta e vedere in anticipo quali modifiche verranno fatte sull'infrastruttura.

## 14. Perché viene ricreato il piano nello stage Deploy?

**Risposta:** Perché nel frattempo è stata creata la nuova immagine del software e il piano deve recepire l'ultima versione disponibile.

## 15. Che relazione esiste tra Build ID, tag e `APP_VERSION`?

**Risposta:** Il numero identificativo della build viene usato come etichetta per l'immagine Docker e come versione dell'applicazione, così sappiamo sempre quale codice è in esecuzione.

## 16. Perché uno smoke test può fallire dopo un apply riuscito?

**Risposta:** Perché l'infrastruttura può essere configurata correttamente da Terraform, ma l'applicazione potrebbe avere un errore di configurazione interna (come una porta errata) che ne impedisce il corretto funzionamento.

## 17. Perché `workspace: clean: all` rende importante lo state remoto?

**Risposta:** Perché pulisce completamente il disco a ogni esecuzione della pipeline, cancellando ogni file locale; senza lo stato remoto, Terraform perderebbe la memoria delle risorse create.

## 18. Che cosa dimostra l'errore sulla target port?

**Risposta:** Dimostra che un'infrastruttura correttamente applicata non garantisce che il servizio risponda se le porte di comunicazione non coincidono.

## 19. Che cosa elimina `terraform destroy` a fine UD14?

**Risposta:** Elimina tutte e sole le risorse che erano state create e gestite dai file di configurazione di Terraform per quell'unità.
