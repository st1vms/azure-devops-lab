# UD06 — Consegna laboratorio autonomo

## 1. Baseline

- VM: `Attiva`
- Nginx: `Installato`
- HTTP: `Raggiungibile`
- regola NSG: `Allow-HTTP-MyIP`

## 2–4. Guasto, diagnosi, ripristino

- regola introdotta:

```txt
Priority: 200
Name: Deny-HTTP-Auto
Port: 80
Protocol: TCP
Source: MyIp
Destination: Any
Action: Allow
```

- sintomo: VM non più raggiungibile tramite HTTP.

- ipotesi: Una regola di sicurezza con un numero di priorità più basso potrebbe bloccare l'accesso.
- controllo: Verificare le security rules Inbound per regole HTTP deny.
- causa: La regola `Deny-HTTP-Auto` con priorità `200` blocca il traffico di rete verso la porta 80 della VM.
- correzione minima: Rimozione della regola di deny.
- verifica: Utilizzare IP Flow Verify per verificare il flusso HTTP inbound e vericare la validità della regola allow.

## 5. Monitoring

- metrica: `Percentage CPU`
- intervallo: `15:15PM - 16:00PM`
- aggregazione: `Avg`
- deduzione: Durante il deploy dell'app si è presentato uno spike di utilizzo della CPU.
- cosa non posso dedurre: Una cosa che non posso dedurre da questa metrica è se il traffico di rete ha causato lo spike della CPU.

## 6. VMSS Autoscale

- min: 1
- default: 1
- max: 4
- metrica: CPU media
- condizione: `> 70% 5min`
- azione: `Scale Out 1`
- perché max=4: corrisponde direttamente al vincolo impostato nel requisito iniziale. Significa che, anche se il carico di lavoro o l'uso della CPU continua a rimanere sopra la soglia, il sistema non installerà mai più di 4 istanze complessive.

## 7. App Service scaling

- A: Scale up
- B: Azure Monitor Autoscale
- C: Automatic Scaling
- D: Scale out manuale

## 8. Backup policy

- frequenza: Giornaliera
- orario: 22:00 UTC
- retention:

  - Giornaliera: 7 giorni
  - Settimanale: 4 settimane
  - Mensile: 12 mesi
  - Annuale: 1 anno

- motivazione: L'esecuzione notturna riduce al minimo l'impatto sulle prestazioni durante le ore operative. La struttura di retention multilivello garantisce un ripristino rapido per incidenti recenti, offrendo al contempo una copertura a lungo termine per conformità normativa e audit senza occupare spazio di archiviazione eccessivo.

## 9. HA / Backup / DR

- A: **HA**. L'alta disponibilità garantisce la resilienza del sistema in presenza di guasti ai singoli componenti hardware o istanze.
- B: **Backup**. Il Backup conserva copie punto-nel-tempo dei dati che consentono di ripristinare uno stato integro precedente all'errore.
- C: **DR**. Il Disaster Recovery gestisce eventi catastrofici o interruzioni su larga scala che compromettono l'intera data center o regione geografica primaria, occupandosi di far ripartire l'intero workload in una seconda regione.

## 10. RPO / RTO

- RPO: 15 minuti
- RTO: 60 minuti
