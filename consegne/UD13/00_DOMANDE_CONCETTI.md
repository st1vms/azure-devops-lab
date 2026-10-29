# UD13 — Domande concetti

## 1. Quale collegamento conserva lo state fra la configurazione Terraform e le risorse Azure? Perché una copia locale diventa problematica nel lavoro condiviso?

**Risposta:** Lo state collega ogni blocco scritto nel codice alla risorsa vera e propria creata su Azure. Una copia locale sul proprio computer diventa un problema se più persone lavorano insieme, perché ognuno avrebbe dati diversi e le modifiche potrebbero sovrapporsi o perdersi.

## 2. A che cosa servono backend remoto e locking? Perché usare un backend remoto richiede anche di progettare accessi e protezione dei dati?

**Risposta:** Il backend remoto è uno spazio condiviso dove Terraform salva lo state, mentre il locking serve a bloccarlo per evitare che due persone o pipeline lo modifichino nello stesso momento. Siccome lo state può contenere dati segreti o importanti, bisogna proteggerlo bene decidendo chi può vederlo e modificarlo.

## 3. Come riconosce Terraform una dipendenza implicita? Perché dividere il codice in più file `.tf` non crea automaticamente più moduli?

**Risposta:** Terraform capisce le dipendenze da solo quando un blocco usa un valore preso da un altro (per esempio, il nome di un gruppo di risorse). Dividere il codice in tanti file `.tf` serve solo a leggerlo meglio, ma per Terraform è sempre un unico grande progetto e non crea moduli separati se non lo diciamo esplicitamente.

## 4. Distingui stage, job e step usando un esempio della pipeline IaC

**Risposta:** Lo stage è la macro-fase della pipeline (come la validazione). Il job è un gruppo di operazioni eseguite insieme su una macchina. Lo step è la singola azione specifica, come scaricare il codice o lanciare un comando.

## 5. Perché UD13 usa inizialmente il self-hosted agent? Che cosa deve essere disponibile sulla postazione perché il job possa partire ed eseguire i comandi?

**Risposta:** Usiamo un agent nostro (self-hosted) perché gira sulla nostra postazione di lavoro in WSL2. Per farlo funzionare, la macchina deve essere accesa, WSL deve essere pronto, l'agent deve essere online e gli strumenti necessari (come Terraform) devono essere già installati e pronti all'uso.

## 6. In un team aziendale, che cosa rappresenta un agent pool? Perché tre agent non garantiscono da soli tre job contemporanei?

**Risposta:** Un agent pool è un gruppo di macchine pronte a eseguire i lavori della pipeline. Avere tre agent non significa poter fare sempre tre cose insieme, perché dipende anche da quanti "Parallel Jobs" l'azienda ha acquistato e se ci sono dipendenze tra i compiti.

## 7. Che cosa cambia passando da `pool-ud09-wsl` a `vmImage: ubuntu-latest`, soprattutto per strumenti e persistenza dei file?

**Risposta:** Se usiamo una macchina gestita da Microsoft (`ubuntu-latest`), non dobbiamo preoccuparci di installare gli strumenti perché vengono forniti freschi ogni volta, ma alla fine del lavoro la macchina viene cancellata e non conserva i file locali.

## 8. Che cosa significa `checkout: self`? Perché un file presente sul nostro PC potrebbe mancare nel checkout della pipeline?

**Risposta:** `checkout: self` significa scaricare il codice del progetto dentro la pipeline. Se un file è sul nostro computer ma non è stato salvato in un commit e inviato al repository, la pipeline non potrà vederlo.

## 9. A che cosa servono `Agent.Name`, `Agent.OS` e `Build.SourcesDirectory`? Perché evitare percorsi personali come `~/workspace/azure-devops-lab` nel YAML?

**Risposta:** Queste variabili dicono alla pipeline il nome dell'agent, il sistema operativo e dove si trova la cartella del codice. Evitiamo i percorsi personali perché cambiano da computer a computer, mentre le variabili funzionano per chiunque.

## 10. Qual è la differenza fra `workspace` con `clean: all` e il checkout con `clean: true`? Quali dipendenze esterne al workspace rimangono comunque sul self-hosted?

**Risposta:** `clean: all` pulisce tutta l'area di lavoro dell'agent prima di iniziare, mentre `clean: true` pulisce solo la cartella del codice Git. Sulla macchina restano comunque installati i programmi di base come Terraform e Azure CLI.

## 11. A che cosa serve la Azure Pipelines GitHub App? Perché il suo accesso al repository non autorizza anche il deployment Azure?

**Risposta:** La GitHub App serve a dare il permesso ad Azure DevOps di leggere il codice sorgente da GitHub. Però leggere il codice è una cosa diversa dal creare infrastrutture su Azure, per cui serve un permesso separato.

## 12. A che cosa serve una service connection? Distingui l'autorizzazione della pipeline a usarla dai permessi Azure dell'identità associata

**Risposta:** La service connection permette alla pipeline di collegarsi ad Azure in modo sicuro. Una cosa è dire "questa pipeline può usare la connessione", un'altra è che l'identità collegata abbia davvero il permesso di fare le modifiche su Azure.

## 13. Quale problema risolve Workload Identity Federation rispetto a un client secret statico? Perché l'autenticazione riuscita non garantisce che ogni operazione sia autorizzata?

**Risposta:** La federazione usa token temporanei e sicuri senza bisogno di memorizzare password segrete fisse che possono scadere o essere rubate. Anche se entriamo con successo, possiamo comunque non avere il permesso di toccare una determinata risorsa.

## 14. Perché limitiamo le autorizzazioni al Resource Group di delivery? Perché creare risorse e assegnare ruoli richiedono permessi distinti?

**Risposta:** Limitiamo i permessi a un solo gruppo di risorse per seguire la regola di dare solo lo stretto necessario (minimo privilegio). Creare un oggetto e dare i permessi ad altri sono due azioni diverse e richiedono autorizzazioni separate.

## 15. Che cosa fanno `fmt -check`, `init -backend=false` e `validate`? Perché il loro successo non equivale a un deployment Terraform riuscito?

**Risposta:** Questi comandi controllano che il codice sia scritto bene, formattato correttamente e senza errori logici. Passarli non significa che Terraform abbia creato le risorse su Azure, perché non abbiamo eseguito il comando di applicazione (`apply`).

## 16. Qual è la differenza fra lint Bicep, What-If e deployment? Quale strumento crea l'ACR nella pipeline di questa UD?

**Risposta:** Il lint controlla gli errori nel codice Bicep, il What-If simula cosa succederà, e il deployment fa avvenire la creazione vera e propria. È proprio il deployment Bicep che crea l'ACR nella pipeline.

## 17. Che cosa disabilita `trigger: none`? In che cosa differisce la successiva CI collegata a `main`?

**Risposta:** `trigger: none` ferma l'avvio automatico della pipeline quando facciamo un push. Invece, una CI collegata a `main` fa partire i controlli da sola ogni volta che inviamo del codice sul ramo principale.

## 18. Perché l'ACR viene conservato per UD14? Distingui la creazione del registry, il push dell'immagine e il pull da parte dell'ambiente applicativo

**Risposta:** L'ACR serve dopo, quindi lo teniamo acceso. Creare il registro è una fase, caricarci dentro l'immagine del programma (push) è un'altra, e scaricarla per farla girare (pull) è l'ultima.

## 19. Perché impostiamo `LegacyRegistryPermissions`? Che cosa accadrebbe ai ruoli legacy se il registry fosse configurato nella modalità ABAC?

**Risposta:** Impostiamo questa modalità classica per usare i vecchi ruoli di accesso come `AcrPull` e `AcrPush`. Se usassimo la modalità ABAC più moderna, quei vecchi ruoli non funzionerebbero più e bloccherebbero tutto.

## 20. Quali risorse vanno eliminate a fine UD13 e quali conservate? Perché il cleanup deve rispettare le dipendenze delle unità successive?

**Risposta:** A fine UD13 eliminiamo solo le cose temporanee dell'esercizio, mentre teniamo il gruppo di risorse principale e l'ACR perché servono anche nella UD14.

## 21. Quale ordine segui per diagnosticare una pipeline fallita? Come distingui un problema di agent, checkout, directory, autenticazione e autorizzazione Azure?

**Risposta:** Si parte dall'inizio: controlliamo se la pipeline è partita, se l'agent è attivo, se il codice si scarica bene, se i comandi trovano la cartella giusta e infine se i permessi su Azure sono corretti.
