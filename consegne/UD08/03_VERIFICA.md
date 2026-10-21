# UD08 — Verifica

## Parte A

1. B. un insieme di cultura, pratiche, automazione e feedback
2. A. integrare frequentemente modifiche verificabili
3. B. sposta modifiche nella staging area
4. A. main
5. B. consente di chiedere modifiche prima del merge
6. B. Git non può determinare in sicurezza il contenuto finale
7. B. backend/API
8. A. per vedere le modifiche che entreranno nel prossimo commit

## Parte B

9. La Continuous Delivery assicura che il codice sia sempre pronto per il rilascio in produzione, ma richiede un'approvazione manuale per l'effettiva pubblicazione. Il Continuous Deployment automatizza invece l'intero processo, rilasciando direttamente agli utenti ogni modifica che supera i test automatici senza alcun intervento umano.

10. Lavorare su un feature branch permette di sviluppare modifiche in un ambiente separato e sicuro senza alterare il codice funzionante del ramo principale. Questo isolamento garantisce che il software rimanga sempre stabile e facilita la revisione del lavoro da parte di altri sviluppatori prima dell'integrazione definitiva.

11. Quando vengono aggiunti nuovi commit al ramo head, la Pull Request si aggiorna in modo automatico per includerli. Questo meccanismo permette di raccogliere nuove correzioni e continuare la discussione nello stesso spazio, senza dover chiudere e riaprire continuamente nuove richieste.

12. Durante una code review è essenziale verificare che il codice sia chiaro e facile da leggere per gli altri colleghi. Bisogna controllare l'assenza di errori logici che potrebbero introdurre dei malfunzionamenti nel sistema. È utile assicurarsi che le modifiche rispettino le regole di stile condivise dal team di sviluppo. Infine, occorre verificare che la nuova funzionalità sia accompagnata da test automatici appropriati.

13. Rimuovere i permessi temporanei è una pratica fondamentale per mantenere la sicurezza del sistema e prevenire accessi non autorizzati. Lasciare attive delle credenziali a chi non collabora più al progetto crea una vulnerabilità inutile, aumentando il rischio di modifiche accidentali o di attacchi informatici tramite account inattivi.

14. Il frontend è l'interfaccia grafica e visiva che permette all'utente di sfogliare il catalogo dal proprio browser. Il backend, tramite le API, è il motore logico invisibile che riceve le richieste del frontend e sa come elaborarle. I dati sono le informazioni concrete sui prodotti, come prezzi e disponibilità, memorizzate in modo sicuro in un database. La configurazione rappresenta l'insieme delle variabili e dei parametri tecnici necessari per far dialogare correttamente tutte queste componenti tra loro.

## Parte C

15. Il problema più grave è la presenza del file token.txt, che rappresenta un rischio critico per la sicurezza: le password e i token segreti non devono mai essere condivisi pubblicamente nel codice. Un altro errore è l'inclusione del file di un'altra unità didattica, che dimostra come la Pull Request contenga modifiche estranee al suo vero scopo, creando confusione. Infine, l'assenza di documentazione per i test HTTP rende impossibile per il team capire come verificare che le nuove modifiche funzionino correttamente.

16. Per correggere la situazione, come prima cosa chiederei allo sviluppatore di revocare o disattivare immediatamente il token segreto e di eliminarlo dalla Pull Request. Successivamente, chiederei di rimuovere il file estraneo, in modo da lasciare solo i file necessari (server.py e config.json). Infine, richiederei di scrivere le istruzioni per eseguire i test; solo dopo aver letto la documentazione e aver visto che i test passano con successo sul codice pulito, darei la mia approvazione per il merge.
