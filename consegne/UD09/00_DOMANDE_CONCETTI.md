# UD09 — Risposte alle domande sui concetti

## 1. Perché DevOps non può essere ridotto a un prodotto?

**Risposta:** DevOps non è un software da comprare o un pulsante da premere. È un modo di lavorare, fatto di idee, collaborazione tra persone e processi. Un programma come Azure DevOps aiuta solo a mettere in pratica queste idee.

## 2. Quali sono le tre dimensioni principali che abbiamo associato a DevOps?

**Risposta:** Le tre dimensioni sono Cultura, Processi e Tecnologia. Servono tutte e tre insieme: la cultura fa collaborare le persone, i processi organizzano il lavoro e la tecnologia automatizza i compiti.

## 3. Perché il lifecycle DevOps è rappresentato come un ciclo?

**Risposta:** Perché il lavoro non finisce mai dopo la consegna. Quando il software è online viene controllato, e dai problemi o dai suggerimenti degli utenti nascono nuove idee per ripartire da capo a pianificare.

## 4. Distingui Agile e DevOps

**Risposta:** Agile serve al team di sviluppo per organizzare e dividere il lavoro in piccoli passi veloci. DevOps va oltre: prende quel lavoro e crea un ponte automatico per portarlo fino ai server e agli utenti finali.

## 5. Che cos'è un backlog?

**Risposta:** È una lista ordinata di tutte le cose da fare per un progetto. Contiene le nuove funzioni da creare, i problemi da risolvere e i miglioramenti tecnici.

## 6. Che cos'è uno sprint?

**Risposta:** È un periodo di tempo breve e fisso, come una o due settimane. In questo tempo il team sceglie un po' di cose dal backlog e le completa del tutto.

## 7. Distingui Scrum e Kanban

**Risposta:** Scrum organizza il lavoro a tempo usando gli sprint e ruoli precisi. Kanban usa una lavagna visiva con le colonne (da fare, in corso, fatto) per controllare che non ci sia troppo lavoro aperto insieme.

## 8. Distingui Epic, Feature, User Story, Task e Bug

**Risposta:** Un Epic è un obiettivo gigante. La Feature è un pezzo importante di questo obiettivo. La User Story descrive cosa vuole l'utente. La Task è l'azione pratica del programmatore. Il Bug è la spiegazione di un errore da correggere.

## 9. A che cosa servono gli Acceptance Criteria?

**Risposta:** Sono le regole scritte che dicono esattamente cosa deve fare la funzione per essere considerata giusta. Servono a capire senza dubbi quando un lavoro è davvero finito.

## 10. Perché il Version Control è importante anche per IaC e pipeline YAML?

**Risposta:** Perché anche le infrastrutture e le automazioni sono scritte come codice. Salvandole su Git possiamo vedere chi ha fatto modifiche, tornare indietro se ci sono errori e lavorare in gruppo senza sovrascriverci.

## 11. Distingui build e artifact

**Risposta:** La build è l'azione o il processo che trasforma i file sorgente in qualcosa di pronto. L'artifact è il file finale ottenuto da questa trasformazione, come un pacchetto ZIP o un'immagine Docker.

## 12. Distingui unit test, integration test e smoke test

**Risposta:** L'unit test controlla un pezzettino piccolo di codice da solo. L'integration test controlla se più pezzi funzionano bene insieme. Lo smoke test è un controllo velocissimo per vedere se l'applicazione si accende e risponde.

## 13. Che cosa significa shift-left?

**Risposta:** Significa fare i controlli e i test il prima possibile, già dal proprio computer. Trovare un errore all'inizio costa molto meno che trovarlo quando il software è già usato dai clienti.

## 14. Definisci Continuous Integration

**Risposta:** È la pratica di unire spesso il proprio codice con quello dei colleghi. Ogni volta che si invia il codice, una procedura automatica fa la build e passa i test per scoprire subito se ci sono errori.

## 15. Distingui Stage, Job e Step

**Risposta:** È la pratica di unire spesso il proprio codice con quello dei colleghi. Ogni volta che si invia il codice, una procedura automatica fa la build e passa i test per scoprire subito se ci sono errori.

## 16. Distingui Continuous Delivery e Continuous Deployment

**Risposta:** Nella Continuous Delivery il software è sempre pronto per essere pubblicato, ma serve un'approvazione manuale per farlo. Nel Continuous Deployment anche l'invio in produzione avviene in automatico senza approvazioni.

## 17. Distingui Dockerfile, image e container

**Risposta:** Il Dockerfile è il foglio di ricetta con le istruzioni. L'image è la torta pronta e congelata (il pacchetto finale). Il container è la fetta di torta nel piatto che stai mangiando adesso (l'applicazione in funzione).

## 18. Che cos'è un registry?

**Risposta:** È un magazzino o un archivio online dove si salvano e si collezionano le immagini Docker per poterle poi scaricare quando servono.

## 19. Che problema risolve un orchestrator?

**Risposta:** Aiuta a gestire tantissimi container insieme in automatico. Si occupa lui di riavviarli se si rompono, di crearne altri se serve e di distribuire il traffico degli utenti.

## 20. Che cos'è Infrastructure as Code?

**Risposta:** Significa creare server e servizi cloud scrivendo codice in dei file di testo, invece di premere i tasti a mano sul sito del cloud.

## 21. Che cosa aggiunge DevSecOps al lifecycle?

**Risposta:** Aggiunge controlli di sicurezza automatici in tutto il percorso di sviluppo, invece di fare la verifica di sicurezza soltanto alla fine prima di pubblicare.

## 22. Che cos'è una DevOps toolchain?

**Risposta:** È la catena di tutti gli strumenti scelti da un team per lavorare insieme, per esempio usando GitHub per il codice, Docker per i pacchetti e Azure per il server.

## 23. Quali sono i cinque principali servizi Azure DevOps?

**Risposta:** Sono Azure Boards per i compiti, Azure Repos per il codice, Azure Pipelines per le automazioni, Azure Test Plans per le prove manuali e Azure Artifacts per i pacchetti.

## 24. A che cosa serve Azure Boards?

**Risposta:** Serve per organizzare il lavoro del team con schede e colonne, assegnare i compiti e vedere a che punto sono le attività.

## 25. Perché nel corso usiamo GitHub invece di Azure Repos?

**Risposta:** Usiamo GitHub perché è il posto standard dove teniamo il codice originale. Usare anche Azure Repos creerebbe solo duplicati inutili e confusione.

## 26. Distingui Azure Test Plans e test automatici in pipeline

**Risposta:** Azure Test Plans serve agli utenti per organizzare e registrare i test fatti a mano. I test automatici della pipeline sono comandi veloci eseguiti dal computer durante la build.

## 27. Distingui Azure Artifacts e Azure Container Registry

**Risposta:** Azure Artifacts salva pacchetti di codice come librerie Python o pacchetti NuGet. Azure Container Registry salva invece immagini di container Docker.

## 28. Distingui Organization e Project

**Risposta:** L'Organization è la scatola grande che rappresenta la tua azienda o account. Il Project è una sottoscatola interna dedicata a un singolo lavoro o software.

## 29. Distingui Agent, Agent Pool e Parallel Job

**Risposta:** L'Agent è la macchina che esegue i comandi. L'Agent Pool è un gruppo di più macchine messe insieme. Il Parallel Job è il permesso che stabilisce quante macchine possono lavorare nello stesso momento.

## 30. Distingui Microsoft-hosted e self-hosted Agent

**Risposta:** Il Microsoft-hosted è una macchina virtuale fornita e gestita da Microsoft che viene distrutta dopo l'uso. Il self-hosted è una macchina gestita direttamente da noi dove decidiamo cosa installare.

## 31. Che cos'è una Service Connection?

**Risposta:** È una chiave di accesso sicura salvata su Azure DevOps che gli permette di parlare con servizi esterni, come Azure Cloud o GitHub.

## 32. Perché il PAT di registrazione può essere revocato dopo che l'agent è Online?

**Risposta:** Perché il PAT serve soltanto all'inizio per far conoscere la macchina ad Azure DevOps. Una volta fatta la registrazione, la macchina usa un suo canale sicuro e il PAT non serve più.

## 33. Perché DevOps non coincide con Azure DevOps?

**Risposta:** DevOps è una filosofia di lavoro generale, mentre Azure DevOps è soltanto uno dei tanti strumenti creati da Microsoft per metterla in pratica.

## 34. Qual è la differenza tra Azure Pipelines e Azure Pipelines Agent?

**Risposta:** Azure Pipelines è il regista che organizza il lavoro e decide la scaletta. L'Agent è l'operaio che esegue fisicamente i comandi sulla macchina.

## 35. Qual è la relazione concettuale tra Azure Pipelines Agent, Jenkins Agent, GitHub Runner e GitLab Runner?

**Risposta:** Fanno tutti esattamente lo stesso lavoro in sistemi diversi: sono gli esecutori pratici che scaricano il codice e lanciano i comandi richiesti dalla pipeline.

## 36. Quali attività svolgerà concretamente l'Agent nelle UD13–UD14?

**Risposta:** Eseguirà i test del codice, creerà le immagini Docker, verificherà la configurazione dell'infrastruttura e invierà l'applicazione aggiornata su Azure.

## 37. Perché un Job Microsoft-hosted non dovrebbe dipendere da file lasciati dal Job precedente?

**Risposta:** Perché per ogni nuovo Job Microsoft crea un computer pulito ed elimina quello vecchio. Quindi i file creati prima non esistono più.

## 38. Perché il WSL2 personale del corso non rappresenta la topologia self-hosted tipica di un team?

**Risposta:** Perché in un'azienda vera l'Agent si trova su un server dedicato sempre acceso accessibile a tutti, non sul computer portatile personale del singolo sviluppatore.

## 39. Come può essere organizzato un Agent Pool aziendale?

**Risposta:** Può essere creato raccogliendo più server o macchine virtuali insieme, così se tanti sviluppatori lanciano un lavoro, ci sono più macchine pronte ad aiutare.

## 40. Perché più Agent non implicano automaticamente più Job eseguibili in parallelo?

**Risposta:** Perché serve anche avere la licenza per la concorrenza (il Parallel Job). Se hai tre macchine ma il tuo piano ti permette un solo lavoro alla volta, le altre macchine rimarranno in attesa.
