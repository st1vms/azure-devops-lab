# UD12 — Consegna LAB autonomo

## Baseline

- `terraform plan`: `No changes`
- stato atteso: `No changes`
- stato osservato: `No changes`

## Modifica

- tag aggiunto: `Environment = "Training"`
- plan add: `0`
- plan change: `1`
- plan destroy: `0`
- motivazione change e non recreate: Perché l'aggiunta di un tag non richiede di ricreare lo storage account.

## Apply e verifica

- apply:

```bash
$ terraform apply \
  ud12-change.tfplan

...

Apply complete! Resources: 0 added, 1 changed, 0 destroyed.

Outputs:

resource_group_name = "rg-ud12-tf"
storage_account_name = "stud12t93194552"
storage_primary_blob_endpoint = "https://stud12t93194552.blob.core.windows.net/"
```

- tag verificato con Azure CLI:

```bash
az storage account show \
  --resource-group rg-ud12-tf \
  --name "$TF_VAR_storage_account_name" \
  --query tags \
  --output jsonc

{
  "Course": "AZ104",
  "Environment": "Training",
  "ManagedBy": "Terraform",
  "UD": "12"
}
```

## Errore controllato

- riferimento errato: `location`
- messaggio `terraform validate`:

```bash
$ terraform validate
╷
│ Error: Reference to undeclared resource
│
│   on main.tf line 15, in resource "azurerm_storage_account" "lab":
│   15:   location                 = azurerm_resource_group.training.location
│
│ A managed resource "azurerm_resource_group" "training" has not been declared in the root module.
```

- causa: Una risorsa di nome training non è stata dichiarata ma viene comunque referenziata nel codice (`training`).
- correzione: Ripristinare il riferimento corretto alla risorsa giusta (`lab`).
- validate finale:

```bash
$ terraform validate
Success! The configuration is valid.
```

## Git

- `.gitignore` verificato: Si
- state non committato: Si
- lock file: versionato
- commit: eseguito
- push/PR: eseguito

## Cleanup Terraform

- `terraform plan -destroy`: `Plan: 0 to add, 0 to change, 2 to destroy.`
- risorse previste:

```bash
Name             ResourceGroup    Location    Type                               Status
---------------  ---------------  ----------  ---------------------------------  ---------
stud12t93194552  rg-ud12-tf       italynorth  Microsoft.Storage/storageAccounts  Succeeded
```

- `terraform destroy`: `Destroy complete! Resources: 2 destroyed.`
- `az group exists`: `false`
- `terraform state list` finale: Vuoto

## Elementi conservati per le nuove UD13–UD14

- Bicep: Si
- Terraform: Si
- file IaC: Si
- agent configurato: Si
