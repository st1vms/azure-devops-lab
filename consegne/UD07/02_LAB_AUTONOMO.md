# UD07 — Consegna laboratorio autonomo

## 1. Script CLI idempotente

- logica: [qui](scripts/setup-rg.sh)
- prima esecuzione:

```bash
$ ./consegne/UD07/scripts/setup-rg.sh
Il Resource Group non esiste: lo creo.
Location    Name
----------  ------------
westeurope  rg-ud07-auto

Aggiorno i tag...

Stato finale:
Name          Location    State
------------  ----------  ---------
rg-ud07-auto  westeurope  Succeeded
```

- seconda esecuzione:

```bash
$ ./consegne/UD07/scripts/setup-rg.sh
Il Resource Group esiste già: lo riutilizzo.

Aggiorno i tag...

Stato finale:
Name          Location    State
------------  ----------  ---------
rg-ud07-auto  westeurope  Succeeded
```

- verifica: Completata

## 2. PowerShell equivalente

- controllo esistenza: [Aggiunto](scripts/setup-rg.ps1)
- modifica: Modificati i tag
- output:

```powershell
PS /home/user> $RgName = "rg-ud07-auto"
PS /home/user> $Location = "westeurope"
PS /home/user>
PS /home/user> $rg = Get-AzResourceGroup `
>>   -Name $RgName `
>>   -ErrorAction SilentlyContinue
PS /home/user>
PS /home/user> if (-not $rg) {
>>     $rg = New-AzResourceGroup `
>>       -Name $RgName `
>>       -Location $Location
>> }
PS /home/user>
PS /home/user> Update-AzTag `
>>   -ResourceId $rg.ResourceId `
>>   -Tag @{ ManagedBy="Autonomo"; UD="07"} `
>>   -Operation Merge | Out-Null
PS /home/user>
PS /home/user> Get-AzResourceGroup `
>>   -Name $RgName |
>>   Select-Object ResourceGroupName, Location, ProvisioningState, Tags

ResourceGroupName Location   ProvisioningState Tags
----------------- --------   ----------------- ----
rg-ud07-auto      westeurope Succeeded         {[ManagedBy, Autonomo], [UD, 07]}
```

## 3. Activity Log

- operazione: `Write tags`
- status: `Succeded`
- timestamp: `2026-10-20T12:27:59.605971Z`

## 4. KQL

```bash
az monitor log-analytics query \
  --workspace "$LAW_CUSTOMER_ID" \
  --analytics-query 'datatable(
  Component:string,
  Status:string,
  DurationMs:int
)
[
  "WEB","OK",120,
  "API","OK",180,
  "DB","WARN",430,
  "API","WARN",510
]
| summarize
    Requests=count(),
    AvgDuration=avg(DurationMs)
  by Status
| sort by AvgDuration desc' \
  --output table
```

1. Due righe
2. WARN
3. Trasforma un dataset basato su singoli eventi (record individuali) in un dataset aggregato basato su gruppi di sintesi.

## 5. Metrics

- metrica: `Transactions`
- unità: `decimal`
- aggregazione: `Sum`
- dato presente: `4 Transactions at 11:47`
- interpretazione: Spike di transazioni eseguite durante la creazione dello storage account.

## 6. Alert

- scope: Storage Account (`stud0792486394`)
- condition: `Transactions > 0`
- severity: `3`
- evaluation frequency: `PT5M`
- Action Group: `ag-ud07`
- Enabled vs Fired: Un alert Fired indica soltanto che si è verificata la condizione impostata nella regola. Se la soglia è configurata in modo troppo sensibile, può generare "rumore" (alert noise) senza rappresentare un reale problema o un disservizio operativo.

### Risposta quesito attività 6

Una alert rule configurata indica che il sistema di monitoraggio ha le istruzioni attive e sta controllando periodicamente i dati. L'alert fired è l'evento reale in cui la condizione impostata è stata effettivamente soddisfatta.

## 7. Guasto amministrativo

- sintomo: Il comando ritorna errore
- errore:

```bash
(ResourceGroupNotFound) Resource group 'rg-ud07-NON-ESISTE' could not be found.
Code: ResourceGroupNotFound
Message: Resource group 'rg-ud07-NON-ESISTE' could not be found.
```

- ipotesi: Il resource group potrebbe non esistere, o potrebbe essere stato inserito un errore di battitura nel comando.
- controllo: Controllare se il comando non presenta errori di battitura, e successivamente verificare l'esistenza del resource group.
- correzione: Correggere il comando se errato, o creare il resource group inesistente
- verifica: Verifica se il comando `az group show` ritorna il gruppo correttamente.

## 8. Runbook

### Sintomo

Comportamento inatteso in script di automazione o pipeline CI/CD dove una risorsa esistente risulta non visibile (i.e. errore `ResourceNotFound`).

### Contesto

Azure CLI

### Controlli

1. Controllare account/subscription.
2. Controlare nome RG.
3. Controllare nome resource ID/nome.

### Comandi

#### 1) Controllo account subscription

```bash
# Verifica l'account loggato
az account show --output table

# Mostra le sottoscrizioni accessibili
az account list --output table
```

Se la sottoscrizione attiva non corrisponde a quella target, impostare il contesto corretto:

```bash
az account set --subscription "<SUBSCRIPTION_ID_O_NOME>"
```

#### 2) Controllo nome RG

Verificare l'esistenza del Resource Group e la corretta sintassi del nome:

```bash
# Controlla se il resource group esiste
az group show --name "<NOME_RG>" --output table

# Mostra tutti i resource groups nella sottoscrizione attiva
az group list --query "[].name" --output table
```

#### 3) Controllo resource ID/nome

Verificare il resource ID e la presenza della risorsa all'interno del RG:

```bash
# Cerca la risorsa nella sottoscrizione attiva
az resource list -zname "<NOME_RISORSA>" --output table

# Verifica informazioni dettagliate sulla risorsa usando l'ID
az resource show --ids "/subscriptions/<ID_SOTTOSCRIZIONE>/resourceGroups/<NOME_RG>/providers/<PROVIDER_NAMESPACE>/<TIPO_RISORSA>/<NOME_RISORSA>" --output table
```

### Activity Log

Ispezionare i log delle attività per verificare se la risorsa è stata eliminata, spostata o se si sono verificati errori di propagazione dei ruoli RBAC.

```bash
# Interroga l'Activity Log per operazioni recenti di delete o gestione
az monitor activity-log list \
  --resource-group "<NOME_RISORSA>" \
  --offset 1d \
  --query "[?contains(authorization.action, 'delete') || contains(authorization.action, 'write')].{Time:eventTimestamp, Caller:caller, Action:authorization.action, Status:status.value}" \
  --output table
```

### Interpretazione

Qualora l'account sia associato a un tenant o sottoscrizione errati, si tratta di un problema di contesto sessione, mentre se la risorsa esiste ma si trova altrove, l'errore risiede nella specifica del Resource Group, o in una sintassi errata del nome o del Resource ID. Infine, se i comandi di ricerca non restituiscono risultati, si può interrogare l'Activity Log per verificare se la risorsa è stata eliminata o se il deployment iniziale è fallito. La mancata visibilità di una risorsa esistente segnala l'assenza dei ruoli RBAC necessari per l'identità in uso.

### Correzione minima

Aggiornamento del contesto della sessione e correzioni delle variabili di ambiente

### Verifica

Confermare la visibilità e lo stato operativo della risorsa:

```bash
az resource show \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --name "<NOME_RISORSA>" \
  --resource-type "<TIPO_RISORSA>" \
  --query "{Name:name, Id:id, ProvisioningState:properties.provisioningState}" \
  --output table
```

### Cleanup

Rimuovere le variabili temporanee e ripristinare il contesto originario se necessario.

## 9. Cleanup

- rg-ud07-auto: eliminato
- rg-ud07-auto-ps: eliminato
