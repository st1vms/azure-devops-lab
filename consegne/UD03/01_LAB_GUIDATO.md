# Consegna UD03 — Laboratorio guidato

## Contesto anonimizzato

- sottoscrizione e tenant verificati: Si
- percorso Entra eseguito: A
- resource group temporaneo: Si

## Identità e assegnazione RBAC

| Principal anonimizzato | Ruolo | Scope | Diretta/ereditata | Motivo |
|---|---|---|---|---|
| admin@<omitted>.onmicrosoft.com | Global Administrator | Directory | Ereditata | Account amministrativo primario |

Descrivi gli oggetti letti o creati, l'autorizzazione necessaria e l'accesso effettivo osservato.

- Utente (`cea-lab-565151`): Rappresenta l'identità che effettua l'accesso in piattaforma, per la creazione è necessario il ruolo User Administrator o Global Administrator.

- Gruppo (`grp-cea-readers-565151`): Raggruppa gli utenti e permessi, consente di assegnare l'accesso a un insieme gestibile di principal, per la creazione è necessario il ruolo User Administrator o Groups Administrator o Global Administrator.

- Prima assegnazione RBAC (`Reader`):  Scopo: `/subscriptions/<omitted>/providers/Microsoft.Authorization/roleDefinitions/acdd72a7-3385-48ef-bd42-f606fba81ae7`.

Verifica assegnazione ruolo:

```bash
RG_SCOPE="$(az group show --name "$LAB_RG" --query id --output tsv)"
az role assignment list \
  --scope "$RG_SCOPE" \
  --include-inherited \
  --query "[].{Role:roleDefinitionName,PrincipalType:principalType,Scope:scope}" \
  --output table

Role    PrincipalType    Scope
------  ---------------  -----------------------------------------------------------------------------------------
Owner   User             /subscriptions/<omitted>
Reader  Group            /subscriptions/<omitted>/resourceGroups/rg-cea-identity-565151
```

- Budget (`budget-cea-565151`): Budget di 50€ mensile assegnato al seguente scope (`rg-cea-identity-565151`), con soglia all'80% della spesa attuale, l'autorizzazione necessaria è `Microsoft.Consumption/budgets/write`. Il cost analysis non mostra niente perché nessuna spesa è stata registrata.

- Creazione Lock `CanNotDelete` (`lock-cea-delete`): Le autorizzazioni necessarie per creare lock sono Owner o User Access Administrator.

Verifica creazione Lock:

```bash
$ az lock list \
  --resource-group "$LAB_RG" \
  --query "[].{Name:name,Level:level,Notes:notes}" \
  --output table

Name             Level         Notes
---------------  ------------  ---------------
lock-cea-delete  CanNotDelete  Lock temporaneo
```

Verifica del lock:

```bash
$ az group delete --name "$LAB_RG" --yes

(ScopeLocked) The scope '/subscriptions/<omitted>/resourcegroups/rg-cea-identity-565151' cannot perform delete operation because following scope(s) are locked: '/subscriptions/<omitted>/resourceGroups/rg-cea-identity-565151'. Please remove the lock and try again.
Code: ScopeLocked
Message: The scope '/subscriptions/<omitted>/resourcegroups/rg-cea-identity-565151' cannot perform delete operation because following scope(s) are locked: '/subscriptions/<omitted>/resourceGroups/rg-cea-identity-565151'. Please remove the lock and try again.
```

Verifico sei il gruppo esiste ancora:

```bash
az group exists --name "$LAB_RG"

true
```

### Risposta sezione 5

L'elenco mostra un'assegnazione per il ruolo "Reader" che riporta il valore "This resource" nella colonna "Scope",
Non sono visibili ruoli ereditati, il tipo di principal è un gruppo (`grp-cea-readers-565151`) e lo scope di origine è il resource group `rg-cea-identity-565151` che coincide con lo Scope mostrato in tabella.

### Risposta sezione 8

```bash
az role assignment list \
  --scope "$RG_SCOPE" \
  --include-inherited \
  --query "[].{Role:roleDefinitionName,PrincipalType:principalType,Scope:scope}" \
  --output jsonc \
  | sed -E 's#/subscriptions/[^/]+#/subscriptions/<omitted>#g'

[
  {
    "PrincipalType": "User",
    "Role": "Owner",
    "Scope": "/subscriptions/<omitted>
  },
  {
    "PrincipalType": "Group",
    "Role": "Reader",
    "Scope": "/subscriptions/<omitted>/resourceGroups/rg-cea-identity-565151"
  }
]
```

## Governance e costi

- tag e significato: Identifica la coppia chiave-valore associata alla risorsa o al gruppo.
- lock e operazione impedita: Specifica quale operazione viene bloccata.
- stato di Cost Analysis: Descrive la spesa accumulata fino a questo momento e la previsione dei costi.
- budget creato o limitazione documentata: Si
- motivo per cui il budget non blocca la spesa: Un budget serve soltanto a generare notifiche per persone o sistemi automatizzati quando la spesa supera una soglia, ma di per se non blocca automaticamente la spesa e non spegne le risorse.

## Cleanup

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

## Rilevanza professionale

Spiega come distinguere autenticazione, autorizzazione RBAC e blocco di governance.

L'autenticazione verifica l'identità dell'utente (risponde alla domanda "Chi è?"). L'autorizzazione determina i permessi di accesso e le operazioni consentite sulle risorse in base al ruolo assegnato (risponde alla domanda "Cosa può fare?"). Mentre il blocco di governance protegge le risorse da modifiche o eliminazioni accidentali, ha priorità assoluta e scavalca anche i permessi massimi concessi dall'RBAC (come anche Owner).
