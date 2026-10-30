# UD13 — Risposte ai concetti di Continuous Integration

## 1. Qual è lo scopo principale della Continuous Integration?

**Risposta:** La Continuous Integration serve a verificare e unire automaticamente le modifiche al codice in modo ripetibile, controllando che tutto funzioni senza errori manuali.

## 2. Perché eseguiamo i test prima della build Docker?

**Risposta:** Perché se il codice ha errori e i test falliscono, è inutile sprecare tempo a costruire e pubblicare l'immagine del contenitore.

## 3. Che cosa significa realmente una pipeline verde?

**Risposta:** Significa che tutti i controlli automatici impostati sono stati superati, ma non garantisce che il software sia perfetto o privo di bug.

## 4. Perché `Build.BuildId` è più utile di `latest` come tag dell'immagine?

**Risposta:** Perché il numero progressivo permette di risalire esattamente alla versione della pipeline che ha creato quell'immagine specifica.

## 5. Qual è la differenza tra `sc-azure-ud13-15` e `sc-acr-ud14`?

**Risposta:** La prima serve a gestire le risorse generali su Azure, mentre la seconda è una connessione Docker per autenticarsi verso il registro dei container.

## 6. Perché l'admin user dell'ACR rimane disabilitato?

**Risposta:** Perché si usa la Workload Identity Federation per motivi di sicurezza, evitando di salvare username e password in chiaro nel file YAML.

## 7. Qual è l'effetto del trigger sul branch `main`?

**Risposta:** Fa partire automaticamente la pipeline ogni volta che viene fatto un nuovo commit o un merge sul ramo principale.

## 8. Perché due Job Microsoft-hosted distinti effettuano entrambi il checkout del repository?

**Risposta:** Perché girano su macchine virtuali separate e temporanee, quindi ognuno deve scaricare il proprio codice sorgente per lavorare.

## 9. Che cosa significa che un Job Microsoft-hosted riceve un ambiente temporaneo?

**Risposta:** Significa che la macchina virtuale viene creata nuova per il lavoro e viene distrutta alla fine, senza lasciare file salvati per il futuro.

## 10. Qual è la differenza fra responsabilità dell'Agent e responsabilità della service connection?

**Risposta:** L'Agent esegue fisicamente i comandi e i task, mentre la service connection fornisce l'identità e i permessi per accedere ai servizi esterni.

## 11. Perché verifichiamo `python3 --version` e `docker --version` nei Job?

**Risposta:** Per assicurarci che gli strumenti necessari siano presenti nell'ambiente prima di iniziare la vera lavorazione.

## 12. Quando utilizziamo il file YAML self-hosted di fallback?

**Risposta:** Lo usiamo quando la versione Microsoft-hosted non è disponibile e dobbiamo appoggiarci al nostro computer con WSL2.

## 13. A cosa serve `workspace.clean: all` nel fallback self-hosted?

**Risposta:** Serve a ripulire la cartella di lavoro prima di iniziare, evitando che vecchi file rimasti dalle esecuzioni passate diano problemi.

## 14. Che cosa fa `Docker@2` con `buildAndPush`?

**Risposta:** Costruisce l'immagine del contenitore e la carica direttamente nel registro di Azure in un unico passaggio.

## 15. In quale ordine conviene leggere i log quando una pipeline fallisce?

**Risposta:** Conviene procedere dal livello più grande al più piccolo: Stage, Job, Step, comando e infine il messaggio di errore.

## 16. Perché un errore nei test non deve portarci immediatamente a controllare ACR?

**Risposta:** Perché se il test fallisce all'inizio, la pipeline si ferma prima ancora di arrivare alla parte che riguarda il registro dei container.

## 17. Che cosa dimostra il test failure intenzionale del laboratorio autonomo?

**Risposta:** Dimostra che la pipeline blocca il processo se trova un errore, ma che la qualità dipende sempre da quanto sono buoni i test scritti.

## 18. Perché non eliminiamo ACR e immagini al termine della preparazione CI?

**Risposta:** Perché quell'immagine è l'artefatto pronto che servirà nella lezione successiva per fare il deployment.

## 19. In che modo l’immagine pubblicata dalla CI prepara il successivo deployment con Terraform?

**Risposta:** Fornisce il pacchetto software già pronto e testato che Terraform andrà a distribuire nell'infrastruttura.
