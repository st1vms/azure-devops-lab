# UD06 — Consegna laboratorio guidato

## VM

- regione selezionata: `denmarkeast`
- size selezionata: `Standard_B1s`
- image: `ubuntu-24_04-lts`
- size: `Standard_B1s`
- private IP: `172.16.0.4`
- public IP: `9.205.248.22` (`vm-ud06-linux-ip`)
- NIC: `vm-ud06-linux178`
- subnet: `snet-vm` (address range 172.16.0.0 - 172.16.0.255)
- OS disk: `vm-ud06-linux_OsDisk_1_a9b7ee887d1445f0bab6199aa655bf43`

## Accesso e workload

- SSH: Si
- Nginx: `nginx/1.24.0`
- test localhost:

```bash
curl -I http://localhost

HTTP/1.1 200 OK
Server: nginx/1.24.0 (Ubuntu)
Date: Mon, 19 Oct 2026 10:53:52 GMT
Content-Type: text/html
Content-Length: 615
Last-Modified: Mon, 19 Oct 2026 10:53:36 GMT
Connection: keep-alive
ETag: "6ad5f6b0-267"
Accept-Ranges: bytes
```

- test esterno:

```bash
$ curl -I "http://9.205.248.22"

HTTP/1.1 200 OK
Server: nginx/1.24.0 (Ubuntu)
Date: Mon, 19 Oct 2026 10:55:32 GMT
Content-Type: text/html
Content-Length: 615
Last-Modified: Mon, 19 Oct 2026 10:53:36 GMT
Connection: keep-alive
ETag: "6ad5f6b0-267"
Accept-Ranges: bytes
```

- IP Flow Verify: `Access allowed`

- regola responsabile: `Allow-HTTP-MyIP` nel NSG `vm-ud06-linux-nsg`

## Azure Monitor

- metrica VM: `Percentale CPU`
- intervallo: `12:00PM - 2:30 PM`
- aggregazione: `Avg`
- osservazione: `Andamento lineare con consumo CPU minimo costante durante l'intera durata dell'intervallo`

- metrica VM: `Network In Total`
- intervallo: `12:00PM - 2:30 PM`
- aggregazione: `Avg`
- osservazione: `Spike ale 12:55PM durante l'accesso SSH per poi ritornare su un andamento minimo costante`

- metrica VM: `Network Out Total`
- intervallo: `12:00PM - 2:30 PM`
- aggregazione: `Avg`
- osservazione: `Leggero spike durante l'accesso ad SSH, con valore nullo costante per la restante durata dell'intervallo`

## VMSS / Autoscale

- min: `1`
- default: `1`
- max: `3`
- metrica: `Percentage CPU`
- soglia: `> 70 avg 5m`
- azione: `Scale Out 1`
- perché serve un max:

### Risposta lla domanda della sezione 11

#### Perché impostare un massimo?

**Risposta:** Il limite massimo è importante per evitare di istanziare troppe istanze quando non necessario o quando potrebbe risultare rischioso. Un limite massimo può prevenire quindi costi imprevisti, ma può anche mitigare contro attacchi DDoS che mirano a saturare le infrastrutture. Può inoltre proteggere contro bug del codice e loop infiniti.

## App Service

- App Service Plan: `F1`
- tier: `Free`
- Web App: `ud06-web-1792414304-2457`
- hostname: `ud06-web-1792414304-2457.azurewebsites.net`
- test HTTPS: Riuscito

## Scaling App Service

| Modalità | Basata su |
|---|---|
| Manual | Conteggio fisso di istanze impostato manualmente dall'utente |
| Azure Monitor Autoscale | Regole definite dall'utente su metriche prestazionali (es. CPU, memoria) o programmazioni orarie |
| Automatic Scaling | Volume di traffico HTTP in ingresso gestito automaticamente dalla piattaforma Azure |

## Azure Monitor App Service

- metrica: `Requests`
- osservazione: `Spike durante richiesta HTTPS`

- metrica: `Response`
- osservazione: `Spike durante richiesta HTTPS`

## Backup

- Recovery Services vault: `vault991`
- Frequenza ipotizzata: `RPO 1 ora`
- Orario: Schedulazione oraria continua nell'arco delle 24 ore
- Retention: 7 giorni per i ripristini ad alta frequenza (snapshot orari) + 30 giorni per i backup giornalieri consolidati
- Motivazione: Garantire un RPO di 1 ora riduce al minimo la perdita di dati per carichi di lavoro operativi e critici. La retention oraria a breve termine copre gli incidenti operativi imminenti, mentre il consolidamento giornaliero ottimizza i costi di archiviazione nel vault.
- Recovery point: Stato temporale generato al termine di ogni job di backup eseguito con successo.
- Backup reale avviato?: no — non previsto nella UD

## HA / Backup / DR

- Scenario A: High Availability
- Scenario B: Backup
- Scenario C: Disaster Recovery

## Cleanup

- Resource Group eliminato: Si
- `az group exists`: false
