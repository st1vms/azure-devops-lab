# UD09 — Verifica individuale

## Parte A — Scelta singola

### 1. DevOps è principalmente

B. un insieme di cultura, pratiche e tecnologie che collegano sviluppo, delivery e operation

### 2. Agile e DevOps

C. Agile riguarda soprattutto lavoro iterativo/adattivo; DevOps estende il flusso a delivery e operation

### 3. Un backlog è

A. un elenco ordinato di lavoro da realizzare

### 4. Continuous Integration significa principalmente

B. integrare frequentemente e verificare automaticamente build/test

### 5. Un artifact è

B. un risultato di build destinato a una fase successiva

### 6. Continuous Deployment si distingue dalla Continuous Delivery perché

B. può portare automaticamente in produzione ogni modifica che supera i gate previsti

### 7. Un container registry conserva principalmente

B. container image

### 8. Un orchestrator serve principalmente a

A. gestire scheduling, repliche, scaling e lifecycle di workload containerizzati

### 9. Azure Boards supporta principalmente

A. planning e tracking del lavoro

### 10. Nel nostro percorso il repository sorgente rimane

B. GitHub

### 11. Un agent è

B. il processo/macchina che esegue un job

### 12. Un parallel job rappresenta

A. la capacità di eseguire job contemporaneamente

## Parte B — Risposte brevi

### 13. Distingui Scrum e Kanban

Scrum è un framework Agile che organizza il lavoro in cicli brevi e fissi chiamati sprint, definendo ruoli ed eventi precisi. Kanban invece è un metodo visivo basato su una bacheca a colonne che serve a monitorare il flusso continuo del lavoro e a limitare le attività in corso (WIP limit) per evitare blocchi o sovraccarichi.

### 14. Distingui Epic, Feature, User Story e Task

Questi elementi formano una gerarchia per organizzare il lavoro dal generale al particolare. L'Epic è un obiettivo molto grande, che viene diviso in Feature, cioè funzionalità importanti del prodotto. Ogni Feature contiene le User Story, che descrivono un bisogno dal punto di vista dell'utente, e infine le Task sono le singole attività pratiche e tecniche da svolgere per completare la storia.

### 15. Distingui build e artifact

La build è il processo che trasforma il codice sorgente in qualcosa di eseguibile o pronto all'uso, come la compilazione del codice o la creazione di un'immagine Docker. L'artifact è il risultato finale e concreto prodotto dalla build (ad esempio un file ZIP, un pacchetto o una container image) che viene salvato e distribuito nei vari ambienti senza doverlo ricreare ogni volta.

### 16. Distingui unit test, integration test e smoke test

L'unit test controlla una piccola parte di codice isolata, come una singola funzione. L'integration test verifica che più componenti diversi funzionino bene insieme, ad esempio un'API e il suo database. Lo smoke test è un controllo veloce fatto subito dopo il rilascio per capire se il servizio è raggiungibile e risponde correttamente alle funzioni base.

### 17. Che cosa significa shift-left?

Shift-left significa anticipare i controlli e i test il più presto possibile nel ciclo di sviluppo. Invece di scoprire un errore solo quando il programma è già in produzione, si cerca di trovarlo subito sul computer dello sviluppatore, nella Pull Request o durante la Continuous Integration, così correggerlo è più facile, veloce e sicuro.

### 18. Distingui Stage, Job e Step

Sono i tre livelli che compongono una pipeline. Lo Stage è una grande fase logica del processo, come "Build" o "Deploy". All'interno dello Stage c'è il Job, che è un gruppo di operazioni affidato a un singolo agent. Lo Step è il singolo comando o azione concreta eseguita dentro il Job, come lanciare uno script di test.

### 19. Distingui Azure Repos, Azure Pipelines, Azure Test Plans e Azure Artifacts

Sono quattro servizi diversi della piattaforma Azure DevOps. Azure Repos serve a gestire i repository Git e il codice sorgente. Azure Pipelines automatizza i processi di build, test e rilascio. Azure Test Plans serve a organizzare e gestire i test manuali ed esplorativi, mentre Azure Artifacts permette di conservare e condividere pacchetti software come librerie NuGet, npm o Python.

### 20. Distingui Organization, Project, Agent Pool e Agent

L'Organization è il contenitore principale di Azure DevOps in cui si gestiscono utenti, sicurezza e impostazioni globali. Al suo interno si creano i Project, che sono gli spazi di lavoro dedicati ai singoli progetti. L'Agent è la macchina che esegue materialmente i comandi delle pipeline, mentre l'Agent Pool è il gruppo che raccoglie e organizza più agent per renderli disponibili alle pipeline.

### 21. Distingui Microsoft-hosted e self-hosted Agent

Un Microsoft-hosted agent è una macchina temporanea gestita da Microsoft, già pronta e pulita, che viene creata da zero per ogni Job e poi distrutta. Un self-hosted agent invece è una macchina gestita direttamente da noi (come il nostro ambiente Linux su WSL2), dove l'ambiente rimane persistente e decidiamo noi quali programmi installare e mantenere.

### 22. Perché Grant access permission to all pipelines non è la scelta predefinita consigliabile?

Non è consigliabile per motivi di sicurezza e per rispettare il principio del privilegio minimo (least privilege). Anche se una connessione verso un sistema esterno esiste, non tutte le pipeline devono poterla usare automaticamente: è meglio autorizzare solo le singole pipeline che ne hanno davvero bisogno.

### 23. Perché il PAT di registrazione dell'agent può essere revocato dopo la configurazione?

Il Personal Access Token (PAT) serve unicamente durante il comando iniziale di configurazione per registrare l'agent su Azure DevOps. Una volta completata la registrazione, l'agent non usa più quel token per eseguire i Job successivi, quindi revocarlo subito è una buona pratica di sicurezza che non fa andare offline l'agent.

### 24. Azure Pipelines e Azure Pipelines Agent sono la stessa cosa? Spiega la differenza

No, non sono la stessa cosa perché lavorano su due livelli diversi. Azure Pipelines è il servizio che organizza, coordina e decide quando e dove far partire il lavoro definito nella pipeline. L'Azure Pipelines Agent invece è il componente installato su una macchina che riceve gli ordini e lancia fisicamente i comandi sul sistema operativo.

### 25. Associa correttamente

```txt
Azure Pipelines -> Azure Pipelines Agent
Jenkins -> Jenkins Agent
GitHub Actions -> Runner
GitLab CI/CD -> GitLab Runner
```

### 26. Perché Jenkins viene citato nella UD09 anche se non lo utilizzeremo operativamente?

Jenkins viene citato per far capire che concetti come pipeline, job, agent, build e test sono principi generali del mondo DevOps e non appartengono solo a Microsoft. Conoscere questo schema ci permette di capire la differenza tra orchestratore ed esecutore e di orientarci facilmente anche su altri strumenti oltre ad Azure DevOps.

### 27. Quali compiti svolgerà concretamente un Agent nelle UD13–UD14?

Nella UD13 l'agent eseguirà la validazione del codice infrastrutturale (IaC con Terraform e Bicep), farà girare i primi Job di pipeline e preparerà i test per la Continuous Integration. Nella UD14 invece eseguirà i test automatici Python, costruirà l'immagine Docker facendone il push su Azure Container Registry, eseguirà il deployment dell'applicazione e lancerà lo smoke test finale.

### 28. Perché prepariamo sia self-hosted sia Microsoft-hosted?

Prepariamo entrambi per imparare a usarli in modo consapevole e confrontarne le differenze pratiche. Il self-hosted ci permette di avere subito un ambiente persistente sotto il nostro controllo per capire fisicamente dove girano i comandi, mentre abilitare il Microsoft-hosted ci permette di lavorare anche con gli ambienti temporanei e puliti gestiti direttamente dal cloud di Microsoft.

## Parte C — Scenario

> Il portale mostra agent-wsl-01 Offline. La registrazione era stata completata correttamente e il PAT è già stato revocato. In WSL2 nessun processo run.sh è attivo.

### 29. Qual è la prima causa da verificare e quale azione eseguiresti?

La prima causa è semplicemente che il processo dell'agent non è in esecuzione su WSL2, perché essere registrato non significa essere attivo. Quando lo script run.sh viene chiuso o terminato, l'agent passa subito allo stato Offline sul portale. L'azione da eseguire è aprire il terminale WSL2, entrare nella cartella dell'agent e avviare nuovamente il comando ./run.sh per rimetterlo in ascolto dei Job e farlo tornare Online.

### 30. Perché non creeresti subito un nuovo PAT e non riconfigureresti l'agent?

Non serve creare un nuovo PAT né rilanciare `./config.sh` perché la registrazione iniziale era già andata a buon fine. Il PAT viene usato soltanto una volta durante la fase di registrazione e non serve per far girare l'agent o eseguire i Job successivi. Riconfigurare tutto da capo sarebbe quindi un passaggio inutile, dato che basta riavviare `./run.sh` per riportare l'agent Online anche con il PAT revocato.

## Parte D - Mappa finale

### Mappa finale

| Area | Strumento del percorso |
|---|---|
| Planning | Azure Boards |
| Version Control | GitHub |
| CI/CD | Azure Pipelines |
| Container | Docker |
| Registry | Azure Container Registry |
| IaC | Bicep + Terraform |
| Runtime | Azure Container Apps |
| Monitoring | Azure Monitor |
