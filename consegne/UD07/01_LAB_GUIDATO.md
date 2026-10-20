# UD07 — Consegna laboratorio guidato

## CLI

- prima esecuzione script:

```bash
$ bash "$COURSE_UD07/script/ud07-cli-admin.sh"
Il Resource Group non esiste: lo creo.
Location    Name
----------  ----------------
westeurope  rg-ud07-cli-test

Aggiorno i tag...

Stato finale:
Name              Location    State
----------------  ----------  ---------
rg-ud07-cli-test  westeurope  Succeeded
```

- seconda esecuzione:

```bash
$ bash "$COURSE_UD07/script/ud07-cli-admin.sh"
Il Resource Group esiste già: lo riutilizzo.

Aggiorno i tag...

Stato finale:
Name              Location    State
----------------  ----------  ---------
rg-ud07-cli-test  westeurope  Succeeded
```

- comportamento idempotente: Verificato, l'idempotenza garantisce che eseguire un'operazione una sola volta o ripeterla più volte produca esattamente lo stesso stato finale sul sistema, senza generare effetti collaterali indesiderati.

- esempio JMESPath:

```bash
$ az group show \
  --name "$LAB_RG" \
  --query "{Name:name,Location:location,Provisioning:properties.provisioningState}" \
  --output table
Name             Location    Provisioning
---------------  ----------  --------------
rg-ud07-monitor  westeurope  Succeeded
```

- quando usare `tsv`: Usare tsv è più conveniente quando bisogna fare il parsing delle informazioni ritornate dall'operazione, utilizzando comandi come `grep`.

## PowerShell

- `Get-AzContext` verificato: Si
- Resource Group test: Verificato
- prima esecuzione:

```powershell
PS /home/user> $RgName = "rg-ud07-ps-test"
PS /home/user> $Location = "westeurope"
PS /home/user> $rg = Get-AzResourceGroup `
>>   -Name $RgName `
>>   -ErrorAction SilentlyContinue
PS /home/user> if (-not $rg) {
>>     $rg = New-AzResourceGroup `
>>       -Name $RgName `
>>       -Location $Location
>> }
PS /home/user> Update-AzTag `
>>   -ResourceId $rg.ResourceId `
>>   -Tag @{ ManagedBy="PowerShell"; UD="07"; State="Verified" } `
>>   -Operation Merge | Out-Null
PS /home/user> Get-AzResourceGroup `
>>   -Name $RgName |
>>   Select-Object ResourceGroupName, Location, ProvisioningState, Tags

ResourceGroupName Location   ProvisioningState Tags
----------------- --------   ----------------- ----
rg-ud07-ps-test   westeurope Succeeded         {[ManagedBy, PowerShell], [UD, 07], [State, Verified]}
```

- seconda esecuzione:

```powershell
PS /home/user> $RgName = "rg-ud07-ps-test"
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
>>   -Tag @{ ManagedBy="PowerShell"; UD="07"; State="Verified" } `
>>   -Operation Merge | Out-Null
PS /home/user>
PS /home/user> Get-AzResourceGroup `
>>   -Name $RgName |
>>   Select-Object ResourceGroupName, Location, ProvisioningState, Tags

ResourceGroupName Location   ProvisioningState Tags
----------------- --------   ----------------- ----
rg-ud07-ps-test   westeurope Succeeded         {[ManagedBy, PowerShell], [UD, 07], [State, Verified]}
```

- perché il controllo `if` è utile: Perché controlla se il gruppo non esiste prima di crearlo, rendendo il comando idempotente, questo permette di evitare effetti collaterali indesiderati come la creazione di un gruppo duplicato.

## Log Analytics

- workspace:

```bash
$ az monitor log-analytics workspace show \
  --resource-group "$LAB_RG" \
  --workspace-name "$LAW" \
  --query "{Name:name,Location:location,State:provisioningState}" \
  --output table
Name            Location     State
--------------  -----------  ---------
law-ud07-18676  northeurope  Succeeded
```

- regione: `northeurope`
- query `print`:

```bash
$ az monitor log-analytics query \
  --workspace "$LAW_CUSTOMER_ID" \
  --analytics-query "print Course='AZ-104', UD=7, Status='OK'" \
  --output table
Course    Status    TableName      UD
--------  --------  -------------  ----
AZ-104    OK        PrimaryResult  7
```

- query `datatable`:

```bash
$ az monitor log-analytics query \
  --workspace "$LAW_CUSTOMER_ID" \
  --analytics-query "datatable(Component:string,Status:string)[
    'API','OK',
    'DB','WARN',
    'WEB','OK'
  ]
  | summarize Count=count() by Status" \
  --output table
Count    Status    TableName
-------  --------  -------------
2        OK        PrimaryResult
1        WARN      PrimaryResult
```

- risultato sintetico: Le query mostrano due messaggi di stato "OK" e un log di warning.

## Activity Log

- evento osservato: `Update resource group`
- status: `Started`
- timestamp: `2026-10-20T08:54:26.9824741Z`
- dati personali omessi: sì

## Diagnostic Setting

- esito: AzureActivity non ancora popolata nel time range osservato.
- destinazione: Send to Log Analytics workspace
- AzureActivity disponibile: sì
- fallback usato, se necessario:

## Metrics

- Storage Account: `stud0792486394`
- metrica: `UsedCapacity`
- unità: `Bytes`
- aggregazione: `Average`
- punto dati disponibile: sì
- interpretazione: Misura lo spazio totale occupato nello storage account.

## Alert

- nome: `alert-ud07-storage-transactions`
- scope corretto: sì/no
- condition: `Transactions > 0`
- severity: `3 - Informational`
- Action Group: presente `ag-ud07`
- perché non è necessario che sia Fired: Fired significa che la condizione è stata effettivamente soddisfatta. Enabled significa che la regola è attiva e può essere valutata.

## Correlazione

- modifica osservata: Aggiornamento tag del resource group.
- evento Activity Log: `2026-10-20T09:36:57.6717036Z  Create/Update Storage Account  Succeeded`
- la correlazione prova causalità?: no
- motivazione: La correlazione indica solo che due eventi si sono verificati nello stesso intervallo di tempo o in sequenza, di per se non prova la causalità.
