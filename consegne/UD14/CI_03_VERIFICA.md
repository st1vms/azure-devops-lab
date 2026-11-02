# UD14 — Verifica

## 1. Perché Test deve precedere BuildPush?

**Risposta:** I test servono a verificare che il codice funzioni senza errori. Farli prima del build evita di perdere tempo a costruire e pubblicare un'immagine di un'applicazione che non funziona.

## 2. Che cosa significa pipeline verde?

**Risposta:** Significa che tutti i passaggi previsti dalla pipeline (come test, build e rilascio) sono stati completati con successo, senza alcun errore.

## 3. Perché usiamo `Build.BuildId` come tag?

**Risposta:** Perché il Build ID è un numero unico per ogni esecuzione. Ci permette di riconoscere subito quale versione del codice si trova dentro l'immagine e nella Container App.

## 4. Quale service connection usa Docker@2?

**Risposta:** Il task `Docker@2` richiede una specifica Docker Registry service connection. Tuttavia, nella nuova architettura preferiamo non usarlo e sfruttare l'Azure Resource Manager service connection.

## 5. Perché ACR admin user può rimanere disabilitato?

**Risposta:** Perché non abbiamo bisogno delle password fisse dell'amministratore dell'ACR; ci colleghiamo in modo sicuro usando direttamente l'identità della service connection di Azure.

## 6. Se Test fallisce, ha senso controllare i permessi ACR? Perché?

**Risposta:** No, non ha senso. Se i test falliscono, la pipeline si blocca subito e non arriva alla fase di pubblicazione (BuildPush), quindi il problema è nel codice e non nei permessi.

## 7. Quale evento attiva la CI configurata?

**Risposta:** Di solito la pipeline si attiva automaticamente quando viene fatto un push di codice sul repository o una pull request.

## 8. Perché non eseguiamo cleanup al termine del blocco CI?

**Risposta:** Perché le risorse e le immagini create servono anche per le fasi successive, come il deployment e i test finali; il cleanup si fa solo alla fine con una pipeline apposita.

## 9. Perché Microsoft-hosted è il percorso principale della CI UD14?

**Risposta:** Perché usa macchine virtuali gestite da Microsoft, già pronte all'uso e pulite, senza bisogno di configurare computer locali.

## 10. Perché due Job Microsoft-hosted non devono condividere implicitamente file locali?

**Risposta:** Perché ogni Job viene eseguito su una macchina virtuale indipendente e pulita; se vogliamo passare file da un job all'altro, dobbiamo farlo esplicitamente con gli artefatti.

## 11. Quando si usa il fallback self-hosted?

**Risposta:** Si usa quando non si usano le macchine Microsoft-hosted e si preferisce affidarsi a un agent installato e configurato sul proprio computer.

## 12. Perché `workspace: clean: all` è importante sul fallback self-hosted?

**Risposta:** Perché pulisce completamente la cartella di lavoro prima di ogni avvio, evitando che vecchi file rimasti dalle esecuzioni precedenti diano problemi.

## 13. Distingui Agent e Docker Registry service connection.

**Risposta:** Distingui Agent e Docker Registry service connection.

## 14. Perché controlliamo `python3 --version` e `docker --version` nei Job?

**Risposta:** Perché controlliamo `python3 --version` e `docker --version` nei Job?

## Gate

- UD14_AGENT_MODE: Self hosted
- pipeline CI riuscita: Si
- ACR/tag: Si
