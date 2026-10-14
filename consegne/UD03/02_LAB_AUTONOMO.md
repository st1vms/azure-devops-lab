# Consegna UD03 — Laboratorio autonomo

## Analisi dell'accesso

| Principal anonimizzato | Ruolo | Scope | Origine | Accesso effettivo |
|---|---|---|---|---|
| Gruppo Microsft Azure Entra ID dedicato al team FinOps | Reader e Cost Management Reader | Resource Group (LAB_RG) |  | |

## Attività

1. Ho scelto il ruolo Reader perché consente la sola visualizzazione delle risorse. Il ruolo Contributor l'ho escluso perché autorizza la creazione, modifica e cancellazione delle risorse, e anche Il ruolo Owner è escluso perché aggiunge la capacità di gestire gli accessi (RBAC), violando i requisiti di sicurezza richiesti.

2. Di seguito l'output di `az role assignment list --scope "$RG_SCOPE" --include-inherited --output table`:

```txt
Principal                        Role                    Scope
-------------------------------  ----------------------  -----------------------------------------------------------------------------------------
<omitted>                        Owner                   /subscriptions/<omitted>
grp-cea-readers-565151           Reader                  /subscriptions/<omitted>/resourceGroups/rg-cea-identity-565151
grp-cea-readers-565151           Cost Management Reader  /subscriptions/<omitted>/resourceGroups/rg-cea-identity-565151
```

L'output mostra che le assegnazioni di ruolo del gruppo Reader e Cost Management Reader sono state assegnate correttamente al resource group come assegnazione diretta,
mentre l'assegnazione con il ruolo Owner è ereditata.

3. Nel portale Azure, la sezione Access control (IAM) classifica le assegnazioni nella colonna Scope. Un'assegnazione è diretta se lo scope corrisponde esattamente al resource group (LAB_RG). È ereditata se lo scope fa riferimento a un livello superiore, come la Subscription o il Management Group. L'assegnazione temporanea di un ruolo Reader non riduce eventuali privilegi più ampi. Il sistema RBAC di Azure utilizza un modello additivo per i permessi di concessione (Allow).

4. Budget summary:

```txt
Name budget-cea-565151
Scope rg-cea-identity-565151 (Resource group)
Filters -
Amount 50.00 EUR
Period Resets monthly
Creation date 10/1/2026
Expiration date 9/30/2028

Alert conditions:

Type: Actual cost
% of budget: 80%
Amount: 40€
Action group: None
Action group type: None
```

5. `az group delete --name "$LAB_RG" --yes --no-wait` ritorna errore, questo vuol dire che il lock funziona.
Mentre `az group show --name "$LAB_RG"` permette di leggere correttamente le informazioni del gruppo, il permesso di lettura funziona.

## Diagnosi dei casi

Per ogni caso separa sintomo, causa probabile, verifica, correzione e risultato atteso.

### Caso A

- Sintomo: Impossibile esegure comandi Azure CLI a causa di un errore che richiede il setup dell'account.

- Causa probabile: L'utente non ha effettuato l'accesso alla CLI, oppure il token di session è scaduto.

- Controllo: Eseguire il comando `az account show`. Se l'account non è connesso, restituirà un errore o richiederà il login.

- Correzione: Eseguire `az login` per avviare l'autenticazione interattiva tramite browser.

- Risultato atteso: Il terminale dovrebbe restituire un array JSON con i dettagli della sottoscrizione autenticata.

### Caso B

- Sintomo: Un'operazione fallisce indicando che l'azione `roleAssignments/write` non è autorizzata.

- Causa probabile: Il principal tenta di assegnare un ruolo, ma non ha i permessi per farlo.

- Controllo: Controllare i permessi sullo scope target.

- Correzione: Richiedere ad un amministratore di assegnare all' account del principal il ruolo "User Access Administrator" sullo scope specifico in cui il principal deve operare.

- Risultato atteso: Il comando di assegnazione del ruolo viene eseguito senza restituire errore.

### Caso C

- Sintomo: Un errore si verifica durante il tentativo di eliminare una risorsa, un resource group o una subscription.

- Causa probabile: Potrebbe essere stato applicato un lock di tipo `CanNotDelete` o `ReadOnly`.

- Controllo: Ispezionare i lock attivi.

- Correzione: Rimuovere il lock dal gruppo o dalla risorsa.

- Risultato atteso: La risorsa o lo scope viene rimosso con successo.

## Budget, lock e cleanup

Spiega funzione e limiti dei tre controlli e documenta l'ordine di rimozione degli oggetti temporanei.

Il budget monitora la spesa e invia notifiche alle soglie definite, ma è puramente passivo; non ferma le risorse ne blocca i costi senza le automazioni necessarie.
Il lock come `CanNotDelete` previene l'eliminazione accidentale di risorse o gruppi, ma non ne impedisce la modifica, l'avvio delle risorse o la continua generazione dei costi.

### Documentazione Cleanup

Registra rimozione degli oggetti temporanei e verifica finale del resource group.

- Rimozione lock:

```bash
LOCK_ID="$(az lock list --resource-group "$LAB_RG" --query "[?name=='lock-cea-delete'].id | [0]" --output tsv)"
test -n "$LOCK_ID" && az lock delete --ids "$LOCK_ID"
az lock list --resource-group "$LAB_RG" --output table
```

L'ultimo comando non ritorna output, quindi il lock risulta correttamente eliminato.

- Eliminazione resource group:

```bash
az group delete --name "$LAB_RG" --yes --no-wait
az group wait --name "$LAB_RG" --deleted
az group exists --name "$LAB_RG"
```

L'ultimo comando ritorna `false`, questo significa che il RG è stato eliminato con successo.

## Risultato finale

- output anonimizzati utilizzati: si
- cleanup verificato: si
- hash abbreviato e messaggio del commit: `fdb2250` "UD03 Risposte alle domande sui concetti"
