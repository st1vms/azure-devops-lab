# Consegna UD05 — Verifica

## Parte A — Scelta singola

Per le domande 1–8 riporta risposta e motivazione.

1. B. /24
2. B. sovrapposizione degli indirizzi
3. B. 200
4. A. subnet e NIC
5. A. consentito da entrambi
6. A. tradurre nomi in indirizzi
7. B. IP Flow Verify
8. B. non garantisce raggiungibilità

## Parte B — Risposte brevi

9. Perché il margine di crescita previene l'esaurimento degli IP durante lo scaling orizzontale, l'aggiunta di risorse o l'integrazione di servizi PaaS. Evita inoltre conflitti legati agli IP riservati dall'architettura di Azure.
10. Il Network security Group (NSG) filtra il traffico definendo quali pacchetti possono passare in base a IP, porte e protocolli. La route (tabella di instradamento) determina la direzione del traffico definendo il salto successivo dei pacchetti. Il DNS è un servizio che mappa i nomi di dominio FQDN nei rispettivi indirizzi IP.
11. La statefulness di un NSG quando una connessione in ingresso viene consentita da una regola traccia la sessione e permette automaticamente il traffico di risposta nella direzione opposta, senza richiedere una regola esplicita di ritorno.
12. Perché centralizza la sicurezza applicando automaticamente la stessa policy a tutte le NIC della subnet. Questo elimina la gestione individuale delle singole interfacce, riduce il rischio di configurazioni errate e semplifica l'audit di compliance.
13. Le verifiche possibili sono: configurazione IP, associazione di NSG e Route Table, e simulazione delle regole e rotte efficaci. Poiché manca il sistema operativo attivo che elabora e risponde ai pacchetti, la prova mancante risulta il test di connettività reale a livello di datapath e stack di rete.

## Parte C — Caso situazionale

14. Il nome della regola è un semplice metadato e non ha alcun impatto sull'ordine di esecuzione.
15. Per consentire il traffico verso l'applicazione senza allentare la sicurezza verso altre destinazioni, modificare la priorità della prima regola a un valore inferiore a 150.
16. Se l'applicazione risulta ancora irraggiungibile dopo l'aggiornamento della priorità, verificare che la regola `AAA-Allow-Web` sia applicata nell'orientamento corretto e che la porta di destinazione corrisponde esattamente. Controllare il firewall del sistema operativo sul server di destinazione e assicurarsi che consenta il traffico sulla porta 443. Verificare inoltre che l'applicazione sia in esecuzione e attiva in ascolto sulla porta TCP 443. Se la regola è gestita da un dispositivo di rete di tipo stateless, verificare la presenza di una regola di ritorno per le porte temporanee nel traffico di risposta. Confermare la presenza di una rotta valida tra la subnet di origine e quella di destinazione. Infine verificare lo stato dei componenti intermedi quali Proxy, Load Balancer o WAF interposti lungo il percorso della connessione.
