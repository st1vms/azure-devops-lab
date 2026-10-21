# UD08 — Risposte domande concetti

## 1. Perché DevOps non coincide con Azure DevOps?

**Risposta:** DevOps è prima di tutto un metodo di lavoro che unisce lo sviluppo, il controllo e il rilascio in un ciclo continuo. Non è semplicemente uno strumento o un software da installare come Azure DevOps, ma un modo per rendere ogni modifica ripetibile, verificabile e sicura.

## 2. Distingui Continuous Integration, Continuous Delivery e Continuous Deployment

**Risposta:** La Continuous Integration consiste nell'unire spesso piccole modifiche al progetto base per testarle subito. La Continuous Delivery mantiene il codice sempre pronto al rilascio, ma richiede una decisione umana esplicita per andare in produzione. La Continuous Deployment automatizza invece anche l'ultimo passaggio, inviando il codice in produzione da solo se supera tutti i test.

## 3. Che differenza c'è tra working tree, staging area e commit?

**Risposta:** La working tree è lo spazio dove lo sviluppatore modifica i file. La staging area è l'area di transito dove si preparano e su scelgono le modifiche che si vogliono includere nel prossimo salvataggio. Il commit registra infine queste modifiche in modo permanente come un'istantanea nella cronologia locale.

## 4. Perché conviene creare un feature branch da main aggiornata?

**Risposta:** Creare un feature branch da una versione aggiornata della base principale permette di separare il nostro lavoro in corso dal codice stabile. In questo modo si parte sempre dalla versione più recente, evitando di lavorare su file vecchi e riducendo il rischio di problemi futuri.

## 5. Che cosa rappresentano base branch e head branch in una Pull Request?

**Risposta:** In una Pull Request, la head branch è il ramo che contiene le nuove modifiche che il collaboratore sta proponendo. La base branch è invece il ramo principale di destinazione, ovvero quello che dovrebbe ricevere e integrare queste nuove modifiche.

## 6. Perché una review non dovrebbe limitarsi a controllare che il codice "funzioni"?

**Risposta:** Una review serve a capire se la modifica risponde davvero ai requisiti iniziali e se il codice è facile da leggere. Bisogna anche controllare che non ci siano segreti esposti, che siano stati previsti dei test e che il nuovo codice non crei malfunzionamenti in altre parti del sistema.

## 7. Che cosa succede a una Pull Request quando il contributor aggiunge un nuovo commit allo stesso branch?

**Risposta:** Quando il collaboratore corregge un file e aggiunge un nuovo commit facendo push sulla stessa branch, la Pull Request si aggiorna automaticamente. Non serve creare una nuova richiesta per far vedere i cambiamenti recenti.

## 8. Che cosa provoca tipicamente un merge conflict?

**Risposta:** Un conflitto si verifica quando due branch diversi modificano la stessa riga di codice in modi tra loro incompatibili. Git non riesce a decidere da solo quale versione mantenere, quindi richiede l'intervento manuale di una persona per capire la logica e scrivere il codice finale.

## 9. Perché l'accesso del collaboratore deve essere rimosso al termine?

**Risposta:** Rimuovere l'accesso serve ad applicare la regola di sicurezza del privilegio minimo. Mantenere un collaboratore nel sistema quando la sua collaborazione è terminata aumenta inutilmente la superficie di rischio del progetto.

## 10. Distingui frontend, backend/API, configurazione e dati nel Catalogo prodotti

**Risposta:** Il frontend è la pagina statica che il browser visualizza, mentre il backend è il server che gestisce le richieste HTTP e le risposte. La configurazione è un file separato con le impostazioni del sistema, e i dati sono semplicemente le informazioni memorizzate sui prodotti.

## 11. Quali endpoint principali espone l'applicazione?

**Risposta:** L'applicazione espone un endpoint di root e un endpoint per controllare se il servizio HTTP risponde correttamente. Espone inoltre due endpoint specifici per i prodotti: uno per ottenere l'intera collezione e uno per cercare un singolo prodotto specifico.

## 12. Perché è utile eseguire git diff prima del commit?

**Risposta:** Usare questo comando aiuta a rileggere visivamente le esatte modifiche che non abbiamo ancora preparato o che stiamo per salvare. Questo ci assicura di creare un commit coerente, inserendo solo i cambiamenti logici necessari senza includere file estranei o errori.
