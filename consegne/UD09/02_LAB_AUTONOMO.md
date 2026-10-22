# UD09 — Consegna laboratorio autonomo

## 1. Organization e Project

- Organization: `azdo-st1vms-01`
- Project: `az900-az104-devops`
- Visibility: `Private`
- Source repository: `st1vms/azdo-agent-ud09`

1. Il Project in Azure DevOps è impostato come privato per proteggere la sicurezza del codice e delle infrastrutture, applicare il principio del minimo privilegio e garantire che solo gli utenti o i gruppi esplicitamente autorizzati dell'Organization possano accedere ai servizi e ai log di esecuzione. Questo isola l'ambiente di lavoro, prevenendo l'esposizione accidentale di dati o modifiche non autorizzate da parte di soggetti esterni.
2. Il source repository rimane su GitHub perché rappresenta già la sorgente di codice autorevole del corso, ed evitarne la duplicazione in Azure Repos previene problemi di sincronizzazione, confusione tra versioni o divergenze. Inoltre, rispecchia un'architettura reale e flessibile dove si sfrutta la migliore combinazione di strumenti (best-of-breed): GitHub gestisce il Version Control e il tracciamento del codice, mentre Azure Pipelines gestisce l'automazione della CI/CD.

## 2. Gruppi

| Gruppo | Scopo | Tutti? |
|---|---|---|
| Project Administrators | Gestione ampia e completa delle impostazioni, delle autorizzazioni e dei servizi all'interno del Project | No |
| Contributors | Permette agli utenti di contribuire normalmente al lavoro di sviluppo, come la creazione e la gestione dei Work Item o il deployment | No |
| Readers | Accesso in sola lettura al Project per consultare lo stato dei lavori e delle pipeline senza poter modificare nulla | No |
| Build Administrators | Privilegi avanzati dedicati alla gestione e all'amministrazione delle risorse di build e delle pipeline | No |

## 3. GitHub integration readiness

- repository: `st1vms/azdo-agent-ud09`
- private: `Si`
- gh auth: Eseguito
- git fetch: Eseguito

1. Non è stata creata per evitare di configurare una connessione personale o basata su metodi obsoleti/meno sicuri (OAuth/PAT) che poi non verrebbero utilizzati nelle pipeline finali. Microsoft raccomanda infatti l'integrazione nativa tramite GitHub App per le pipeline CI/CD.
2. Useremo l'integrazione tramite Azure Pipelines GitHub App, la quale verrà stabilita direttamente da Azure DevOps al momento della creazione della prima pipeline selezionando il repository GitHub
3. Duplicare lo stesso codice in due sistemi diversi introdurrebbe confusione su quale sia la versione autorevole, problemi di sincronizzazione e il rischio di divergenza tra i due repository. Mantenere GitHub come unico source repository garantisce un'unica sorgente della verità (single source of truth).

## 4. Parallel jobs

- hosted: 0
- self-hosted: 1

1. No
2. Uno solo alla volta
3. No

## 5. Agent audit

- pool: `pool-ud09-wsl`
- agent: `wsl-ud09-st1vms`
- status: `Online`
- version: `5.281.0`
- Agent.OS: `Linux`
- Agent.Version: `5.281.0`
- git: `/usr/bin/git`
- python: `/usr/bin/python3`

## 6. Registration authentication audit

- metodo: `PAT`
- status PAT, se applicabile: `Revocato`
1. Il Personal Access Token (PAT) viene utilizzato esclusivamente durante la fase di configurazione e registrazione iniziale per autenticare l'operatore e registrare la macchina nell'Agent Pool. Durante questo processo, l'agent scambia il PAT con credenziali/chiavi OAuth dedicate e token di sessione propri. Di conseguenza, una volta completata la registrazione e avviato il servizio, la revoca del PAT non influisce sulla comunicazione ordinaria tra l'agent e Azure DevOps.
2. Applicando il principio del minimo privilegio (least privilege), un PAT con permessi Full access non è necessario ed è altamente rischioso in caso di esposizione. Per completare la registrazione dell'agent è sufficiente un token con lo scope ristretto Agent Pools (Read & manage).
3. Se le policy di sicurezza dell'Organization bloccano o limitano la creazione dei PAT, indebolire o disabilitare tali policy a livello organizzativo crea una falla di sicurezza permanente per tutti gli utenti. Il Device Code Flow è un'alternativa decisamente più sicura perché: Non richiede di modificare le policy di sicurezza dell'Organization; Sfrutta l'autenticazione diretta e temporanea nel browser tramite l'identità dell'utente; Evita del tutto la creazione e la gestione manuale di segreti a lungo termine o token.

## 7. Offline/Online

- stop: Si
- stato: `Offline`
- restart: Si
- stato: `Online`

## 8. Troubleshooting

1. Verifica: Verificare che il processo dell'agent sia in esecuzione nell'ambiente WSL2.
2. Verificare che l'ambiente WSL2 possa raggiungere l'endpoint di Azure DevOps tramite HTTPS.
3. Controllare che l'URL dell'Organization inserito nella configurazione dell'agent sia esatto.
4. Verificare che l'agent sia associato all'Agent Pool corretto e che il pool esista nel Project o nell'Organization.
5. Assicurarsi che la struttura dei file dell'agent sia integra e che i file di configurazione non siano corrotti o incompleti.
6. Analizzare i log generati dall'agent per individuare l'errore specifico.

## 9. Readiness

| Controllo | PASS/FAIL | Nota |
|---|---|---|
| Organization | PASS | |
| Project | PASS | |
| GitHub readiness | PASS | |
| Hosted | PASS | Hosted status documentato |
| Pool | PASS | Self-hosted pool |
| Agent | PASS | Agent Online |
| PAT / Device Code Flow | PASS | PAT revocato |
| Capability | PASS | Capability controllate |
| Restart | PASS | Restart Online/Offline testato |
| Secrets | PASS | Nessun segreto nel repository |
