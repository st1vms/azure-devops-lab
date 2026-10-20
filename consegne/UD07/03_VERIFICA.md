# UD07 — Verifica

## Parte A

1. A. --query
2. B. tsv
3. B. oggetti
4. A. eventi del control plane della subscription
5. B. instradare segnali diagnostici verso destinazioni
6. B. KQL
7. B. notifiche e azioni associate agli alert
8. B. viene valutata, ma può non essere Fired

## Parte B

9. L'Activity Log registra le operazioni di gestione del control plane, mostrando chi ha eseguito un'azione sulle risorse e con quale esito. Le Metrics sono serie temporali di valori numerici associate al tempo, utilizzate per osservare tendenze sull'uso delle risorse come la CPU o la rete. I Logs contengono invece record più ricchi e dettagliati che includono informazioni di contesto e timestamp, pensati per essere inviati a un ambiente di analisi ed essere interrogati.

10. L'idempotenza indica la proprietà per cui rieseguire una procedura porta allo stato desiderato senza generare errori o effetti collaterali indesiderati. In ambito amministrativo, un esempio è uno script che prima di creare un Resource Group ne verifica l'esistenza: se la risorsa c'è già la riutilizza, altrimenti la crea.

11. Il formato di output `table` in Azure CLI mostra le informazioni organizzate in una tabella formattata per la lettura da parte di una persona. Il formato `tsv` restituisce invece il valore puro separato da tabulazioni e privo di virgolette o parentesi, rendendolo ideale per salvare un dato in una variabile e riutilizzarlo in comandi successivi.

12. La diagnostic setting e il Log Analytics workspace sono distinti perché svolgono ruoli diversi all'interno del flusso dei dati. La diagnostic setting agisce come una regola di instradamento che stabilisce quali categorie di log o metriche inviare e verso quale destinazione. Il Log Analytics workspace è invece l'ambiente di destinazione finale in cui i dati vengono raccolti, conservati e interrogati tramite query KQL.

13. La Alert Rule serve a definire il segnale da osservare, la frequenza e la condizione che stabilisce quando la regola deve scattare. L'Action Group si occupa invece della reazione operativa, definendo quale azione concreta intraprendere quando la regola scatta, come l'invio di un'email o l'avvio di un'automazione.

14. La correlazione temporale indica semplicemente l'ordine cronologico con cui si sono verificati due eventi, ma non dimostra che il primo sia stato la causa del secondo. Un problema scattato dopo una modifica potrebbe dipendere da fattori esterni non collegati, per cui per confermare la causalità servono ulteriori evidenze tecniche e verifiche approfondite sui log.

## Parte C

15. Con certezza si può affermare soltanto la sequenza cronologica degli eventi registrati, ovvero che alle 10:15 la risorsa è stata modificata, alle 10:16 l'Activity Log ha registrato la scrittura con esito positivo, alle 10:20 la metrica è aumentata e alle 10:25 l'alert è passato allo stato Fired. Questi dati confermano esclusivamente l'ordine temporale in cui si sono verificate le singole azioni.

16. Per dimostrare un effettivo legame di causa-effetto è necessario verificare che cosa sia stato modificato nello specifico e accertarsi che la metrica che ha generato l'alert sia tecnicamente collegata a quel cambiamento.

---

## Cleanup finale della UD07

- diagnostic setting subscription: rimossa / non era stata creata
- `rg-ud07-cli-test`: eliminato
- `rg-ud07-ps-test`: eliminato
- `rg-ud07-auto`: assente
- `rg-ud07-auto-ps`: assente
- `rg-ud07-monitor`: eliminato
- controllo finale Resource Group UD07: nessun residuo / residui da verificare
