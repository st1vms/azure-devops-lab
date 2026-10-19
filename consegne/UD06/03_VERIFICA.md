# UD06 — Verifica

## Parte A

1. A. NIC
2. B. VM Scale Set
3. B. scale out
4. A. App Service Plan
5. B. metriche e regole
6. B. Metrics rappresentano valori numerici nel tempo; Logs sono record interrogabili
7. A. Recovery Services vault
8. B. Disaster Recovery

## Parte B

9. Le Availability Zone sono data center fisicamente separati e isolati all'interno della stessa regione Azure, progettati per proteggere i workload da guasti che potrebbero colpire un'intera struttura. L'Availability Set è invece un raggruppamento logico che distribuisce le macchine virtuali su diversi Fault Domain per l'hardware e Update Domain per la manutenzione all'interno dello stesso data center. Il VM Scale Set gestisce un insieme di macchine virtuali identiche, permettendo la gestione coordinata e lo scaling dinamico in base alle esigenze del carico di lavoro.

10. Lo scale up rappresenta un ridimensionamento verticale in cui si aumentano le risorse hardware della singola istanza esistente, ad esempio passando da 2 a 4 vCPU. Lo scale out è un ridimensionamento orizzontale che consiste nell'incrementare il numero complessivo di istanze o macchine virtuali che eseguono l'applicazione.

11. App Service Autoscale, gestito tramite Azure Monitor Autoscale, applica un ridimensionamento basato su regole personalizzate, soglie di metriche specifiche come la CPU oltre il 70%, o pianificazioni temporali. L'Automatic Scaling è una modalità gestita nativamente dalla piattaforma PaaS che adatta in modo dinamico e automatico il numero di istanze in base al traffico in ingresso.

12. L'High Availability comprende le tecnologie pensate per ridurre al minimo il downtime ridondando i componenti dell'infrastruttura in modo che il servizio rimanga sempre attivo. Il Backup è il processo di copia e conservazione dei dati per consentirne il ripristino a uno stato precedente in caso di perdita o danneggiamento. Il Disaster Recovery definisce la strategia e le procedure necessarie a ripristinare un intero servizio, ad esempio tramite failover su una regione secondaria, a seguito di un evento catastrofico.

13. Il Recovery Services vault è il contenitore di gestione in Azure che memorizza i dati di protezione e centralizza la gestione dei backup. La backup policy definisce la pianificazione dell'esecuzione dei backup, la loro frequenza e il periodo di conservazione dei dati salvati. Il recovery point rappresenta lo stato di ripristino salvato, ossia la fotografia dei dati o della VM da cui è possibile effettuare il recupero.

14. L'RPO, ossia Recovery Point Objective, indica la quantità massima di dati espressa in tempo che un'organizzazione è disposta a perdere a seguito di un incidente. L'RTO, ossia Recovery Time Objective, misura invece il tempo massimo ammissibile per ripristinare la piena operatività del servizio dopo un guasto.

## Parte C

15. La causa più probabile è la regola dell'NSG `Deny-HTTP` (priorità `100`) che blocca il traffico inbound sulla porta TCP 80. Poiché entrambe intercettano lo stesso traffico, il pacchetto viene scartato al livello dell'NSG e la regola a priorità `300` non viene mai valutata.

16. Eliminare la regola con priorità 100 (`Deny-HTTP`). Utilizzare lo strumento **IP Flow Verify** di Network Watcher per confermare che l'esito indichi `Access allowed` e mostri come regola applicata la `Allow-HTTP`.
