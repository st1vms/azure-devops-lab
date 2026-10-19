# UD06 — Risposte alle domande sui concetti

## 1. Quali risorse e componenti principali costituiscono una VM Azure?

**Risposta:** Una Virtual Machine Azure è costituita dalle seguenti componenti e risorse fondamentali:

- Image: stabilisce il sistema operativo base.
- Size: definisce le risorse di calcolo assegnate.
- Os Disk: il disco virtuale principale che contiene il sistema operativo e i file di sistema.
- Data Disk: disco virtuale aggiuntivo dedicato alla memorizzazione dei dati e delle applicazioni.
- NIC: l'interfaccia di rete virtuale.

## 2. Perché Public IP e raggiungibilità non sono sinonimi?

**Risposta:** Un indirizzo Public IP fornisce soltanto un punto di entrata raggiungibile pubblicamente da Internet, ma non assicura che il servizio sia effettivamente accessibile. Per garantire la reale raggiungibilità sono necessari ulteriori elementi coordinati, come tabelle di routig, regole di sicurezza e configurazioni valide.

## 3. Distingui Availability Zone, Availability Set e VM Scale Set

**Risposta:** Le **Availability Zones** rappresentano datacenter fisicamente separati e isolati all'interno della stessa regione Azure. Gli **Availability Set** distribuiscono le VM su diversi *Fault Domain* e *Update Domain*. I **VM Scale Set** invece costituiscono un gruppo gestito ed omogeneo di VM identiche che consente il bilanciamento del carico, il deployment coordinato e la gestione dell'autoscaling.

## 4. Qual è la differenza tra scale up e scale out?

**Risposta:** Scale Up è lo scaling verticale, consiste nell'aumentare le risorse hardware della singola istanza. Scale Out invece è lo scaling orizzontale, consiste nell'aumentare il numero complessivo di istante cloni.

## 5. Come può Azure Monitor Autoscale modificare un VM Scale Set?

**Risposta:** Azure Monitor Autoscale modifica dinamicamente il numero di istanze di un VM Scale Set applicando regole definite dall'utente. Queste regole valutano le metriche di prestazione, schedule o orari pianificati e limiti del profilo.

## 6. Qual è la differenza tra App Service Plan e Web App?

**Risposta:** **App Service Plan** rappresenta l'infrastruttura di calcolo (PaaS) e definisce la capacità di calcolo usata dalle applicazioni, la regione di deployment, il sistema operativo, il livello/tier di prezzo, le funzionalità disponibili e il numero di istanze. **Web App** rappresenta l'applicazione software effettiva che viene eseguita all'interno dell'App Service Plan.

## 7. Qual è la differenza tra Azure Monitor Autoscale e App Service Automatic Scaling?

**Risposta:** **Azure Monitor Autoscale** è un meccanismo basato su regole personalizzate definite dall'utente, che valutano metriche specifiche oppure orari pianificati per aggiungere o rimuovere istanze. **App Service Automatic Scaling** è una modalità di ridimensionamento totalmente gestita dalla piattaforma Azure, basata sull'andamento in tempo reale del traffico HTTP. Gestisce automaticamente l'allocazione e il pre-riscaldamento delle istanze.

## 8. Distingui Metrics e Logs/Log Analytics

**Risposta:** Le **Metrics** sono dati numerici leggibili e strutturati raccolti a intervalli regolari, che descrivono lo stato di una risorsa in un preciso momento. I **Logs** o **Log Analytics** sono record di eventi, tracciamenti e registri di diagnostica, archiviati in un *Log Analytics workspace* e analizzabili tramite query complesse utilizzando il linguaggio KQL.

## 9. Qual è il ruolo di Recovery Services vault, backup policy e recovery point?

**Risposta:** Un **Recovery Services vault** è un contenitore di gestione ed archiviazione in cui vengono salvati i dati di ripristino, le configurazioni di protezione e gli storici dei backup per le risorse. La **Backup policy** è l'insieme delle regole di pianificazione che definiscono la frequenza di esecuzione del backup. Il **Recovery point** invece rappresenta lo stato o la copia consistente dei dati salvati in un momento preciso, dal quale è possibile eseguire la procedura di ripristino.

## 10. Distingui High Availability, Backup e Disaster Recovery

**Risposta:** La **High Availability** garantisce la continuità operativa ed evita o riduce al minimo i tempi di inattività attraverso la ridondanza di componenti hardware, applicative e architetturali all'interno della stessa regione. Un **Backup** si occupa di salvare copie coerenti di dati e configurazioni nel tempo per consentirne il recupero. Un piano di **Disaster Recovery** definisce strategie e strumenti per replicare l'intero ambiente di lavoro su un'altra regione o infrastruttura, consentendo di ripristinare il servizio a seguito di eventi catastrofici o guasti su larga scala.

## 11. Che cosa indicano RPO e RTO?

**Risposta:** L'**RPO (Recovery Point Objective)** indica la massima perdita temporale di dati accettabile in seguito a un guasto (es. un RPO di 1 ora indica che è tollerabile perdere al massimo un'ora di dati, obiettivo che può essere soddisfatto tramite backup con opportuna frequenza o altri sistemi di protezione). L'**RTO (Recovery Time Objective)** invece indica il tempo massimo ammissibile entro il quale il servizio o l'infrastruttura deve essere ripristinata e tornare pienamente operativa dopo l'interruzione (es. RTO di 30 minuti).

## 12. Perché una VM "deallocated" può continuare a generare costi?

**Risposta:** Quando una VM si trova nello stato `Stopped (deallocated)`, le risorse di calcolo fisiche vengono rilasciate e non generano più costi di calcolo. Tuttavia, continuano ad essere addebitati i costi relativi alle risorse correlate che permangono allocate per garantire l'integrità del sistema, tra cui: OS Disk, Data Disk, indirizzi pubblici riservati, eventuali altri servizi o risorse collegate.
