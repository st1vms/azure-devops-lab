# UD07 — Risposte alle domande sui concetti

## 1. Perché --query è preferibile a cercare manualmente una stringa nell'output JSON?

**Risposta:** Il parametro `--query` lavora direttamente sulla struttura dell'oggetto JSON distribuito da Azure CLI, estraendo solo le proprietà richieste. Cercare testo manualmente (ad esempio con `grep`) individua solo stringhe di caratteri ed è molto meno affidabile quando si desidera automatizzare una procedura.

## 2. Qual è la differenza tra table e tsv in Azure CLI?

**Risposta:** Il formato `table` organizza i dati in una tabella formattata per la lettura da parte delle persone. Il formato `tsv` restituisce invece solo il valore puro (senza virgolette, parentesi o strutture JSON), ideale per memorizzare il risultato in una variabile e riutilizzarlo in uno script.

## 3. Che cosa significa lavorare con oggetti in PowerShell?

**Risposta:** Significa che i comandi non restituiscono semplice testo, ma strutture dati che contengono proprietà accessibili direttamente (ad esempio `$rg.Location`). È inoltre possibile passare l'intero oggetto da un comando all'altro usando la pipeline.

## 4. Che cosa significa che una procedura amministrativa è idempotente?

**Risposta:** Significa che eseguendo la procedura più volte si ottiene sempre lo stesso stato desiderato, senza creare risorse duplicate o generare errori se la risorsa o la configurazione esiste già.

## 5. Distingui Activity Log, Metrics e Logs

**Risposta:** L'Activity Log registra le operazioni amministrative sul control plane di Azure, ovvero chi ha creato, modificato o eliminato una risorsa e in quale momento. Le Metrics rappresentano valori numerici misurati nel tempo espressi come serie temporali, quali l'utilizzo della CPU o il volume di transazioni. I Logs sono invece record dettagliati contenenti timestamp, stato, operazioni e dettagli approfonditi per l'analisi.

## 6. A che cosa serve un Log Analytics workspace?

**Risposta:** È un ambiente centralizzato in cui raccogliere dati di log provenienti da diverse sorgenti e all'interno del quale è possibile eseguire analisi e ricerche tramite query KQL.

## 7. A che cosa serve una diagnostic setting?

**Risposta:** Funziona come una regola di instradamento che definisce quali specifiche categorie di log o metriche inviare da una risorsa verso una destinazione (ad esempio un Log Analytics workspace).

## 8. Perché Activity Log e AzureActivity non sono esattamente la stessa cosa?

**Risposta:** L'**Activity Log** è il registro generale delle operazioni di Azure consultabile dal Portale o dalla CLI. **AzureActivity** è invece la tabella specifica dentro Log Analytics in cui gli eventi dell'Activity Log vengono memorizzati ed evidenziati via KQL dopo aver configurato una diagnostic setting.

## 9. Distingui Alert Rule e Action Group

**Risposta:** La Alert Rule definisce il segnale da monitorare e la condizione che fa scattare l'allarme quando viene superata una soglia. L'Action Group stabilisce invece l'azione concreta da eseguire quando l'allarme si attiva, come l'invio di un'email, un SMS o la chiamata a un webhook.

## 10. Perché un alert Fired non equivale automaticamente a un incidente?

**Risposta:** Un alert Fired indica soltanto che si è verificata la condizione impostata nella regola. Se la soglia è configurata in modo troppo sensibile, può generare "rumore" (alert noise) senza rappresentare un reale problema o un disservizio operativo.

## 11. Qual è la differenza tra correlazione e causalità?

**Risposta:** La correlazione indica solo che due eventi si sono verificati nello stesso intervallo di tempo o in sequenza. La causalità dimostra invece che il primo evento è stato la causa diretta del secondo.

## 12. Quali sono i passaggi essenziali di un troubleshooting ripetibile?

**Risposta:** I passaggi essenziali prevedono innanzitutto di descrivere il sintomo del problema e chiarire il risultato atteso. Successivamente occorre raccogliere le evidenze, formulare un'ipotesi e verificarla. Infine si applica la modifica minima necessaria, si ripete la verifica dell'esito e si documentano la procedura e la soluzione finale.
