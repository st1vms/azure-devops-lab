# 44. Concetti da conoscere prima del laboratorio Azure

Prima di iniziare il laboratorio UD05 devi saper rispondere senza consultare il documento:

1. Lo switch collega dispositivi all'interno della stessa rete locale (LAN) utilizzando indirizzi MAC. Il router collega reti diverse tra loro instradando il traffico tramite indirizzi IP.
2. L'indirizzo MAC è l'identificativo fisico e permanente dell'hardware di rete (Livello 2). L'indirizzo IP è un identificativo logico assegnato per la comunicazione sulla rete (Livello 3).
3. È la notazione CIDR che indica che i primi 24 bit di un indirizzo IP identificano la rete. Corrisponde alla subnet mask 255.255.255.0.
4. È il nodo (solitamente un router) a cui un dispositivo invia i pacchetti dati diretti verso indirizzi IP esterni alla propria rete locale.
5. Il DHCP (Dynamic Host Configuration Protocol) assegna automaticamente indirizzi IP e altri parametri di configurazione ai dispositivi in rete.
6. Il DNS (Domain Name System) traduce i nomi di dominio leggibili in indirizzi IP necessari per l'instradamento del traffico.
7. Il TCP è orientato alla connessione e garantisce la consegna affidabile e ordinata dei dati. L'UDP non richiede connessione ed è più veloce, ma non garantisce l'arrivo o l'ordine dei pacchetti.
8. Una porta è un costrutto logico che identifica un processo, un servizio o un'applicazione specifica in esecuzione su un dispositivo di rete.
9. Una route è una regola definita in una tabella di routing che determina il percorso che i pacchetti dati devono seguire per raggiungere una rete di destinazione.
10. Un firewall è un sistema di sicurezza che monitora, filtra e blocca il traffico di rete in entrata e in uscita basandosi su regole predefinite.
11. Una VLAN (Virtual LAN) segmenta logicamente una rete fisica locale in domini di broadcast separati, migliorando sicurezza e gestione.
12. La VLAN opera a Livello 2 per segmentare reti locali fisiche. Una VNet è un costrutto cloud a Livello 3 che fornisce un ambiente di rete isolato all'interno di un'infrastruttura cloud.
13. Il NAT traduce gli indirizzi IP privati di una rete locale in uno o più indirizzi IP pubblici per consentire l'accesso a Internet.
14. Una DMZ (Demilitarized Zone) è una sottorete isolata che espone servizi pubblici a Internet, mantenendoli separati per proteggere la rete interna aziendale.
15. Una VPN (Virtual Private Network) stabilisce un tunnel crittografato e sicuro attraverso una rete pubblica, permettendo l'accesso remoto a risorse di rete private.
16. In ambiente Windows, mostra i dettagli completi della configurazione TCP/IP per tutte le interfacce di rete, inclusi indirizzo MAC, IP, gateway, server DNS e stato DHCP.
17. È uno strumento a riga di comando che interroga i server DNS per verificare la corretta risoluzione di un nome di dominio nel relativo indirizzo IP, o viceversa.
18. Il DNS fornisce esclusivamente la traduzione del nome in IP. La comunicazione effettiva richiede routing corretto, assenza di blocchi firewall lungo il percorso e che l'applicazione di destinazione sia attiva e in ascolto sulla porta corretta.
